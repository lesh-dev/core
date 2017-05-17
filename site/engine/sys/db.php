<?php

/**
  * @author Mikhail Veltishchev <dichlofos-mv@yandex.ru>
  * Database management module
  **/
require_once("${engine_dir}sys/string.php");
require_once("${engine_dir}sys/auth.php");

define('XDB_NEW', 'new');
define('XDB_APPROVED_NEW', 'approved_new');
define('XDB_INVALID_ID', '-1');

define('XDB_OVERRIDE_TS', true);
define('XDB_NO_OVERRIDE_TS', false); // default

define('XDB_USE_AI', true);
define('XDB_NO_USE_AI', false); // default

define('XDB_DEBUG_AREA_DISABLED', false);
define('XDB_DEBUG_AREA_ENABLED', true); // default

define('XDB_DEFAULT_DB_PATH', "ank/fizlesh.sqlite3");


/**
  * Helper for obtaining keys that are DB ids from request. Filters all
  * non-numeric characters from input, returns XDB_INVALID_ID (-1) by default
  * or when all characters were filtered.
  **/
function xdb_get_idvar($key, $default_value = XDB_INVALID_ID, $allowed_values = array())
{
    $value = xcms_get_key_or($_GET, $key, '');
    if ($value == XDB_NEW || array_search($value, $allowed_values))
        return $value;
    $value = xcms_filter_nondigits($value);
    if (xu_empty($value))
        return $default_value;
    return $value;
}


/**
  * Helper for obtaining enum values from request. Filters all
  * invalid characters from input.
  **/
function xdb_get_enumvar($key)
{
    $value = xcms_get_key_or($_GET, $key, "");
    $value = preg_replace('/[^a-zA-Z0-9-]/', "", $value);
    return $value;
}


/**
  * Obtains database handle in read-only mode
  **/
function xdb_get()
{
    global $SETTINGS;
    global $content_dir;
    $rel_db_name = xcms_get_key_or($SETTINGS, 'xsm_db_name', XDB_DEFAULT_DB_PATH);
    $db_name = $content_dir.$rel_db_name;

    $db = new SQlite3($db_name, SQLITE3_OPEN_READONLY);
    // enhance LIKE immediately to obtain proper UTF-8 support
    $db->createFunction('LIKE', 'xdb_like', 2);
    return $db;
}


/**
  * Obtains database handle in writeable mode
  **/
function xdb_get_write()
{
    global $SETTINGS;
    global $content_dir;
    $rel_db_name = xcms_get_key_or($SETTINGS, 'xsm_db_name', XDB_DEFAULT_DB_PATH);
    $db_name = $content_dir.$rel_db_name;
    return new SQlite3($db_name, SQLITE3_OPEN_READWRITE);
}


/**
  * Inserts or updates DB record
  * @param $table_name table name to update/insert into
  * @param $primary_keys KV-array of table primary keys
  * @note If PK value has the special value XDB_NEW, the insertion is performed
  * and table should have AI key
  * @param $values KV-array of row values
  * @param $allowed_keys only these keys will be taken from $values
  * @return true on successful update, false on error
  * and autoincremented field id on insertion
  **/
function xdb_insert_or_update($table_name, $primary_keys, $values, $allowed_keys)
{
    $insert = false;
    foreach ($primary_keys as $key => $value)
        if ($value == XDB_NEW)
            $insert = true;
    if ($insert)
        return xdb_insert_ai($table_name, $primary_keys, $values, $allowed_keys);
    else
        return xdb_update($table_name, $primary_keys, $values, $allowed_keys);
}


/**
  * Insert single record into autoincrement table
  * @param $table_name Table name to insert into
  * @param $pk_name primary key name (autoincrement)
  * @param $keys_values KV-array of row values
  * @param $allowed_keys only these keys will be taken from $values
  * @param $override_ts override timestamps (true by default)
  * @param $ignore_ai ignore autoincrement keys, use value from $keys_values
  * @param $outer_db use given external database (not used by default)
  *
  * Special fields,
  * ${table_name}_created,
  * ${table_name}_modifed,
  * are filled using current UTC time value in human-readable form
  * (that can be converted back to timestamp, though)
  * and ${table_name}_changedby representing last user name
  * so they should always present in any table.
  **/
function xdb_insert_ai($table_name, $pk_name, $keys_values, $allowed_keys, $override_ts = XDB_OVERRIDE_TS, $use_ai = XDB_USE_AI, $outer_db = NULL)
{
    $db = ($outer_db === NULL) ? xdb_get_write() : $outer_db;
    $keys = "";
    $values = "";

    if ($override_ts)
    {
        $keys_values["${table_name}_created"] = xcms_datetime();
        $keys_values["${table_name}_modified"] = '';
    }
    // for audit purposes
    $keys_values["${table_name}_changedby"] = xcms_user()->login();

    foreach ($allowed_keys as $key => $unused)
    {
        $value = xcms_get_key_or($keys_values, $key);
        if ($use_ai and $key == $pk_name)
            continue; // skip autoincremented keys
        $keys .= "$key, ";
        $values .= "'".$db->escapeString($value)."', ";
    }
    $keys = substr($keys, 0, strlen($keys) - 2);
    $values = substr($values, 0, strlen($values) - 2);

    $query = "INSERT INTO $table_name ($keys) VALUES ($values)";
    $result = $db->exec($query);
    if ($result)
    {
        $result = $db->lastInsertRowid();
        xcms_log(XLOG_INFO, "[DB] $query");
    }
    else
    {
        $result = false;
        xcms_log(XLOG_ERROR, "[DB] $query");
    }
    if ($outer_db === NULL)
        $db->close();
    return $result;
}


/**
  * Updates one row using given primary keys' values,
  * also updates ${table_name}_modified timestamp
  * @param $table_name Table name to update
  * @param $primary_keys KV-array of table primary keys
  * @param $keys_values KV-array of row values
  * @param $allowed_keys only these keys will be taken from $values
  * @param $override_ts override timestamps (true by default)
  * @param $outer_db use given external database (not used by default)
  *
  * A special field, ${table_name}_modified, will be updated
  * using current UTC time value in human-readable form
  * @sa xdb_insert_ai
  * @return true in case of success, false otherwise
  **/
function xdb_update($table_name, $primary_keys, $keys_values, $allowed_keys, $override_ts = XDB_OVERRIDE_TS, $outer_db = NULL)
{
    $db = ($outer_db === NULL) ? xdb_get_write() : $outer_db;
    $values = "";
    if ($override_ts)
        $keys_values["${table_name}_modified"] = xcms_datetime();
    // for audit purposes
    $keys_values["${table_name}_changedby"] = xcms_user()->login();

    foreach ($keys_values as $key => $value)
    {
        if (!array_key_exists($key, $allowed_keys))
            continue; // skip keys that are not in scheme

        if ($key == "${table_name}_created")
            continue; // never update 'created' field

        if (array_key_exists($key, $primary_keys))
            continue; // skip primary keys

        $values .= "$key = '".$db->escapeString($value)."', ";
    }
    $values = substr($values, 0, strlen($values) - 2);

    $cond = "";
    foreach ($primary_keys as $key => $value)
    {
        $cond .= "($key = '".$db->escapeString($value)."') AND ";
    }
    $cond = substr($cond, 0, strlen($cond) - 5);
    $query = "UPDATE $table_name SET $values WHERE $cond";
    $result = $db->exec($query);
    if ($result)
        xcms_log(XLOG_INFO, "[DB] $query");
    else
        xcms_log(XLOG_ERROR, "[DB] $query");
    if ($outer_db === NULL)
        $db->close();
    return $result ? true : false;
}

/**
  * Retrieves KV-array of values for the given ID from table.
  * @param $table_name Table name to get data from
  * @param $id primary key value (compound keys are not supported)
  * @return KV-array of row values
  * A convention states that primary keys in our tables have
  * special names obtained from table name: ${table_name}_id
  *
  * If the $id has the magic value XDB_NEW, the empty record is
  * returned
  **/
function xdb_get_entity_by_id($table_name, $id)
{
    $db = xdb_get();
    $key_name = "${table_name}_id";


    if ($id != XDB_NEW)
    {
        $idf = preg_replace('/[^-0-9]/', '', $id);
        if (strlen($idf) == 0)
        {
            xcms_log(XLOG_ERROR, "[DB] Cannot fetch entity from '$table_name' with empty or filtered id '$id'.");
            return array();
        }
        $id = $idf;
        $query = "SELECT * FROM $table_name WHERE $key_name = $id";
        $sel = $db->query($query);
        if (!($ev = $sel->fetchArray(SQLITE3_ASSOC)))
        {
            xcms_log(XLOG_ERROR, "[DB] Cannot fetch entity from '$table_name' with id: '$id'. Query: $query.");
            return array();
        }
        $db->close();
    }
    else
    {
        // new record
        $ev = array(
            $key_name => $id,
        );
    }
    return $ev;
}

// FIXME(mvel): fix style and tell Yarik
function query_length($query)
{
    $tmp = $query;
    $count = 0;
    if (!$tmp) {
        return 0;
    }
    while ($tmp->fetchArray())
    {
        ++$count;
    }
    return $count;
}

function resultSetToArray($queryResultSet)
{
    $multiArray = array();
    $count = 0;
    if (!$queryResultSet)
    {
        return array();
    }
    while ($row = $queryResultSet->fetchArray(SQLITE3_ASSOC))
    {
        foreach ($row as $i => $value)
        {
            $multiArray[$count][$i] = $value;
        }
        $count++;
    }
    return $multiArray;
}
// End of code style fixes

function xdb_get_filtered($table_name, $keys)
{
    $db = xdb_get();
    $filter = "1=1";
    foreach ($keys as $key => $value)
        $filter = "$filter AND $key=\"$value\"";
    $query = "SELECT * FROM $table_name WHERE $filter;";
    $sel = $db->query($query);
    if (!($ev = resultSetToArray($sel)))
    {
        xcms_log(XLOG_ERROR, "[DB] Cannot fetch entries from '$table_name' with keys: '$keys'. Query: $query.");
        return array();
    }
    $db->close();
    return $ev;
}

/**
  * Deletes record with the given ID from table.
  * @param $table_name Table name to delete data from
  * @param $id primary key value (compound keys are not supported)
  * @param $outer_db use given external database (not used by default)
  * @return operation result (BUG: db-specific!)
  *
  * A convention states that primary keys in our tables have
  * special names obtained from table name: ${table_name}_id
  *
  * If the $id has the magic value XDB_NEW, the empty record is
  * returned
  **/
function xdb_delete($table_name, $key_value, $outer_db = NULL)
{
    $db = ($outer_db === NULL) ? xdb_get_write() : $outer_db;
    $cond = "${table_name}_id = '".$db->escapeString($key_value)."'";
    $query = "DELETE FROM $table_name WHERE $cond";
    $result = $db->exec($query);
    if ($result)
        xcms_log(XLOG_INFO, "[DB] $query");
    else
        xcms_log(XLOG_ERROR, "[DB] $query");
    if ($outer_db === NULL)
        $db->close();
    return $result;
}

/**
  * Selects first fetched object.
  * Useful when query should typicaly return one record or less.
  * @param $db database handle
  * @param $query query
  **/
function xdb_fetch_one($db, $query)
{
    $sel = $db->query($query);
    if (!($obj = $sel->fetchArray(SQLITE3_ASSOC)))
    {
        xcms_log(XLOG_ERROR, "[DB] Cannot fetch object using query: $query.");
        return array();
    }
    return $obj;
}


/**
  * Shortcut for SELECT COUNT(*) requests
  **/
function xdb_count($db, $query)
{
    $obj = xdb_fetch_one($db, $query);
    if (!$obj)
        return 0;
    return (integer)(xcms_get_key_or($obj, "cnt", "0"));
}


/**
  * UTF8-friendly LIKE operator for SQLite database
  * @note this function is for INTERNAL use only
  * @param $mask LIKE operator mask
  * @param $value value to match
  * @return matches or not (boolean value)
  **/
function xdb_like($mask, $value)
{
    $mask = str_replace(
        array("%", "_"),
        array(".*?", "."),
            preg_quote($mask, "/")
    );
    $mask = "/^$mask$/ui";
    return preg_match($mask, $value);
}


/**
  * Returns whole content of the table in array
  * using given filter (WHERE condition) and order
  * @param table_name table name
  * @param filter WHERE clause
  * @param order ORDER BY clause
  **/
function xdb_get_table($table_name, $filter = '', $order = '')
{
    $db = xdb_get();
    $query = "SELECT * FROM $table_name";
    if (strlen($filter))
        $query .= " WHERE $filter ";
    if (strlen($order))
        $query .= " ORDER BY $order ";
    $sel = $db->query($query);
    $ans = array();
    while ($obj = $sel->fetchArray(SQLITE3_ASSOC))
    {
        $ans[] = $obj;
    }
    $db->close();
    return $ans;
}

/**
  * Returns whole content of the table in associative array by PK
  * using given filter (WHERE condition) and order
  * @param table_name table name
  * @param filter WHERE clause
  * @param order ORDER BY clause
  **/
function xdb_get_table_by_pk($table_name, $filter = '', $order = '')
{
    $ans = xdb_get_table($table_name, $filter, $order);
    $result = array();
    $key_name = "${table_name}_id";
    foreach ($ans as $obj)
    {
        $key = $obj[$key_name];
        $result[$key] = $obj;
    }
    return $result;
}

/**
  * Embedded query debugger
  **/
function xdb_debug_area($query, $enabled = XDB_DEBUG_AREA_ENABLED)
{
    $query = str_replace("\n", " ", $query);
    $query = str_replace("\r", " ", $query);
    $query = str_replace("\t", " ", $query);
    $query = preg_replace("/ +/", " ", $query);
    ?>
    <textarea rows="5" cols="120" style="display: <?php echo ($enabled ? "" : "none"); ?>;"
        id="person-query-debug"><?php echo $query; ?></textarea><?php
}


/**
  * Migration helpers
  * TODO(mvel): unit tests for them
  **/
function xdb_open_db($db_name)
{
    xcms_log(XLOG_INFO, "[DB] Open database '$db_name'");
    return new SQlite3($db_name, SQLITE3_OPEN_READONLY);
}


function xdb_open_db_write($db_name)
{
    xcms_log(XLOG_INFO, "[DB] Open database '$db_name' for WRITING");
    return new SQlite3($db_name, SQLITE3_OPEN_READWRITE);
}


function xdb_get_selector($db, $table_name)
{
    $query = "SELECT * FROM $table_name";
    return $db->query($query);
}


function xdb_drop_column($db, $table_name, $column_name, $create_table)
{
    // create new table
    $db->exec($create_table);
    // copy data
    $sel = xdb_get_selector($db, $table_name);
    $objects = 0;
    while ($obj = $sel->fetchArray(SQLITE3_ASSOC))
    {
        $idn = "${table_name}_id";
        $object_id = $obj[$idn];
        unset($obj[$column_name]); // specific code
        xdb_insert_ai("${table_name}_new", $idn, $obj, $obj, XDB_OVERRIDE_TS, XDB_NO_USE_AI, $db);
        ++$objects;
    }

    // rename table
    $db->exec("DROP TABLE $table_name");
    $db->exec("ALTER TABLE ${table_name}_new RENAME TO $table_name");
    xcms_log(XLOG_INFO, "[DB] Dropped $column_name from $table_name, processed $objects objects");
}


function xdb_vacuum($db)
{
    $db->exec("VACUUM");
    xcms_log(XLOG_INFO, "[DB] Database vacuumed");
}
