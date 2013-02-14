<?php
    /**
      * @author Mikhail Veltishchev <dichlofos-mv@yandex.ru>
      * Database management module
      **/

    /**
      * Obtains database handle in read-only mode
      * TODO: Unhardcode database location ("$content_dir/ank/fizlesh.sqlite3")
      **/
    function xdb_get()
    {
        global $content_dir;
        return new SQlite3("$content_dir/ank/fizlesh.sqlite3", SQLITE3_OPEN_READONLY);
    }

    /**
      * Obtains database handle in writeable mode
      * TODO: Unhardcode database location ("$content_dir/ank/fizlesh.sqlite3")
      **/
    function xdb_get_write()
    {
        global $content_dir;
        return new SQlite3("$content_dir/ank/fizlesh.sqlite3", SQLITE3_OPEN_READWRITE);
    }

    /**
      * Inserts or updates DB record
      * @param $table_name Table name to update/insert into
      * @param $primary_keys KV-array of table primary keys
      * @note If PK value has the special value 'new', the insertion is performed
      * and table should have AI key
      * @param $values KV-array of row values
      * @param $allowed_keys only these keys will be taken from $values
      * @return true on successful update, false on error
      * and autoincremented field id on insertion
      *
      * TODO: Unhardcode database location ("$content_dir/ank/fizlesh.sqlite3")
      **/
    function xdb_insert_or_update($table_name, $primary_keys, $values, $allowed_keys)
    {
        $insert = false;
        foreach ($primary_keys as $key => $value)
            if ($value == "new") $insert = true;
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
      *
      * Two special fields, ${table_name}_created and ${table_name}_modifed
      * are filled using current UTC time value in human-readable form
      * (that can be converted back to timestamp, though)
      * so they should always present in any table
      **/
    function xdb_insert_ai($table_name, $pk_name, $keys_values, $allowed_keys)
    {
        $db = xdb_get_write();
        $keys = "";
        $values = "";

        // override 'created' and 'modified' field
        $unix_time = time();
        $hr_timestamp = date("Y.m.d H:i:s", $unix_time);
        $keys_values["${table_name}_created"] = $hr_timestamp;
        $keys_values["${table_name}_modified"] = '';

        foreach ($allowed_keys as $key => $title)
        {
            $value = xcms_get_key_or($keys_values, $key);
            if ($key == $pk_name)
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
            xcms_log(0, "[DB] $query");
        }
        else
        {
            $result = false;
            xcms_log(0, "[DB:ERROR] $query");
        }
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
      *
      * A special field, ${table_name}_modified, will be updated
      * using current UTC time value in human-readable form
      * @sa xdb_insert_ai
      * @return true in case of success, false otherwise
      **/
    function xdb_update($table_name, $primary_keys, $keys_values, $allowed_keys)
    {
        $db = xdb_get_write();
        $values = "";
        // update '<table-name>-modified' timestamp
        $unix_time = time();
        $hr_timestamp = date("Y.m.d H:i:s", $unix_time);
        $keys_values["${table_name}_modified"] = $hr_timestamp;

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
            xcms_log(0, "[DB] $query");
        else
            xcms_log(0, "[DB:ERROR] $query");
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
      * If the $id has the magic value 'new', the empty record is
      * returned
      **/
    function xdb_get_entity_by_id($table_name, $id)
    {
        $db = xdb_get();
        $key_name = "${table_name}_id";


        if ($id != "new")
        {
            $idf = preg_replace('/[^-0-9]/', '', $id);
            if (strlen($idf) == 0)
            {
                xcms_log(0, "Cannot fetch entity from '$table_name' with empty or filtered id '$id'.");
                return array();
            }
            $id = $idf;
            $query = "SELECT * FROM $table_name WHERE $key_name = $id";
            $sel = $db->query($query);
            if (!($ev = $sel->fetchArray(SQLITE3_ASSOC)))
            {
                xcms_log(0, "Cannot fetch entity from '$table_name' with id: '$id'. Query: $query.");
                return array();
            }
            $db->close();
        }
        else
        {
            // new record
            $ev = array(
                $key_name=>$id
            );
        }
        return $ev;
    }

    /**
      * Deletes record with the given ID from table.
      * @param $table_name Table name to delete data from
      * @param $id primary key value (compound keys are not supported)
      * @return operation result (BUG: db-specific!)
      *
      * A convention states that primary keys in our tables have
      * special names obtained from table name: ${table_name}_id
      *
      * If the $id has the magic value 'new', the empty record is
      * returned
      **/
    function xdb_delete($table_name, $key_value)
    {
        $db = xdb_get_write();
        $cond = "${table_name}_id = '".$db->escapeString($key_value)."'";
        $query = "DELETE FROM $table_name WHERE $cond";
        $result = $db->exec($query);
        if ($result)
            xcms_log(0, "[DB] $query");
        else
            xcms_log(0, "[DB:ERROR] $query");
        $db->close();
        return $result;
    }

    /**
      * UTF8-friendly LIKE operator for SQLite database
      * @note this function is for INTERNAL use only
      * BUG: It should be pre-loaded for every created DB handle
      * like this: $db->createFunction('LIKE', 'xdb_like', 2);
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
      *  This function returns whole content of $table_name, using (if provided) $order and $filter properly.
    **/
    function xdb_get_table($table_name, $order, $filter)
    {
            $db = xdb_get();
            $query = "SELECT * FROM $table_name";
            if($filter)
              $query += " WHERE $filter ";
            if($order)
              $query += " ORDER BY $order ";
            //echo $query;
            //$query += ";";
            $sel = $db->query($query);
            $ans = array();
            while($ev = $sel->fetchArray(SQLITE3_ASSOC))
            {
                $ans[] = $ev;
            }
            return $ans;
    }
?>