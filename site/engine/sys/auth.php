<?php

define('XAUTH_THROW', true);
define('XAUTH_NO_THROW', false);

require_once("${xengine_dir}sys/string.php");
require_once("${xengine_dir}sys/logger.php");
require_once("${xengine_dir}sys/tag.php");

class XcmsUser
{
    private function _file_name($login)
    {
        global $SETTINGS, $content_dir;
        $cd = $SETTINGS["content_dir"];
        if (xu_empty($cd))
            $cd = $content_dir;
        if (xu_empty($cd))
            throw new Exception ("Content directory is not set in SETTINGS. ");
        $fn = "${cd}auth/usr/$login.user";
        return $fn;
    }
    private function _hash($string)
    {
        // TODO: replace md5 with secure hash (sha256)
        return md5($string."saulty!");
    }
    /**
      * Сериализует пользователя
      **/
    private function _save()
    {
        if (!$this->is_valid())
            throw new Exception("Cannot save invalid user. ");

        if ($this->is_null())
            return $this->set_error("Cannot save NULL user. ");

        $fn = $this->_file_name($this->login());
        if (!xcms_save_list($fn, $this->dict))
            throw new Exception("Cannot save user to file '$fn'. ");

        return true;
    }
    function is_valid()
    {
        return $this->valid;
    }
    function set_valid()
    {
        $this->valid = true;
    }
    /**
      * Конструктор. Создает пользователя с заданным именем.
      * @param login имя пользователя
      **/
    public function XcmsUser($login)
    {
        $fn = $this->_file_name($login);
        if (file_exists($fn))
        {
            $this->dict = xcms_get_list($fn);
            $this->valid = true;
        }
        else
        {
            $this->dict = array();
            $this->dict["login"] = $login;
            $this->valid = false;
        }
        $this->is_superuser = false;
    }
    /**
      * Возвращает текущее имя пользователя
      **/
    function login()
    {
        return $this->dict["login"];
    }

    function set_param($key, $value)
    {
        if (!in_array($key, array("password", "email", "name", "creator", "creation_date")))
            $this->check_rights("admin");
        if ($key == "email")
        {
            $cand_login = $this->find_by_email($value);
            if ($cand_login !== NULL && $cand_login != $this->login())
                return $this->set_error("Невозможно изменить email: пользователь с такой почтой '$value' уже существует. ");
        }
        $this->dict[$key] = $value;
        $this->_save();
    }
    function param($key)
    {
        return @$this->dict[$key];
    }
    /**
      * Возвращает электронную почту пользователя
      **/
    function email()
    {
        return @$this->dict["email"];
    }
    /**
      * Возвращает список групп, к которым принадлежит пользователь.
      * Внимание! Использовать эту команду для проверки прав НЕЛЬЗЯ!
      **/
    function groups()
    {
        return explode(EXP_COM, @$this->dict["groups"]);
    }

    function check_rights($group, $throw_exception = XAUTH_THROW)
    {
        $group = str_replace("#", "", $group);
        if ($group == "all")
            return true;
        if ($group == "registered" && $this->is_valid())
            return true;
        if ($this->is_superuser())
            return true;
        if (in_array($group, $this->groups()))
            return true;
        if ($throw_exception)
            throw new Exception("User doesn't belong to group $group to perform this action");
        return false;
    }

    /**
      * Возвращает true, если пользователь кривой.
      **/
    function is_null()
    {
        if (strlen($this->login()))
            return false;
        return true;
    }
    /**
      * Обнуляет пользователя
      **/
    function set_null()
    {
        $this->check_rights("admin");
        $this->dict = array();
    }
    /**
      * Делает пользователя суперпользователем, для которого любые проверки прав успешны.
      **/
    function set_superuser()
    {
        // This is only way to get SU flag from code!
        $this->is_superuser = true;
    }
    /**
      * Указывает, является ли пользователь суперпользователем.
      **/
    function is_superuser()
    {
        return $this->is_superuser;
    }
    /**
      * Добавляет пользователя в группу.
      * @param $login имя пользователя
      * @param $group группа, в которую будет добавлен пользователь $login
      * @return true, если пользователь успешно добавлен, false, если пользователь уже
      * принадлежит указанной группе. В случае ошибок будет кинуто исключение.
      **/
    function add_to_group($login, $group)
    {
        $group = str_replace("#", "", $group);
        $this->check_rights("admin");
        $user = new XcmsUser($login);
        if (in_array($group, $user->groups()))
            return false;
        $user->dict["groups"] = implode(",", array_merge($user->groups(), array($group)));
        $user->_save();
        return true;
    }
    /**
      * Удаляет пользователя из группы.
      * @param $login имя пользователя
      * @param $group имя группы, из которой надо исключить пользователя
      * @return true, если пользователь успешно исключён, false, если пользователя
      * в этой группе не было. В случае ошибки будет кинуто исключение.
      **/
    function remove_from_group($login, $group)
    {
        $group = str_replace("#", "", $group);
        $this->check_rights("admin");
        $user = new XcmsUser($login);
        if (!in_array($group, $user->groups()))
            return false;
        $user->dict["groups"] = implode(",", array_diff($user->groups(), array($group)));
        $user->_save();
        return true;
    }
    /**
      * Выставляет значение последней ошибки
      * TODO: Это неправильная политика. Исключения должны лететь в любом случае
      * а уж ловить их, или перехватывать только в глобальном обработчике -- дело
      * шаблона
      **/
    function set_error($error, $throw_exception = XAUTH_THROW)
    {
        $this->error = $error;
        if ($throw_exception)
            throw new Exception($error);
        return $error;
    }
    /**
      * Возвращает последнюю ошибку
      **/
    function get_last_error()
    {
        return $this->error;
    }
    /**
      * Задает новый пароль пользователю
      * TODO: Зачем хранить plaintext_password? Очень непонятное поведение,
      * скорее всего небезопасное.
      * @param password новый пароль
      * @param old_password старый пароль (если передаётся, то сначала проверяется
      * на соответствие старому паролю
      **/
    function passwd($password, $old_password = false, $throw_exception = XAUTH_THROW)
    {
        if (!strlen($password))
            return $this->set_error("Пароль не должен быть пустым. ", $throw_exception);

        if (!xcms_check_password($password))
            return $this->set_error("Password contains invalid characters. ", $throw_exception);

        if ($old_password !== false)
        {
            if ($this->dict["password"] != $this->_hash($old_password))
                return $this->set_error("Старый пароль указан неверно. ", $throw_exception);
        }

        $this->dict["password"] = $this->_hash($password);
        $this->plaintext_password = $password;
        $this->_save();
        return true;
    }
    /**
      * Создает нового пользователя
      * @param login логин нового пользователя
      * @param email email нового пользователя
      * @return экземпляр созданного только что пользователя
      **/
    function create($login, $email)
    {
        $login_check_result = xcms_check_user_name($login);
        if (!$login_check_result["valid"])
            return $this->set_error($login_check_result["reason"]);

        $this->check_rights("admin");
        if (file_exists($this->_file_name($login)))
            return $this->set_error("Пользователь '$login' уже существует. ");
        if ($this->find_by_email($email) !== NULL)
            return $this->set_error("Пользователь с электронной почтой '$email' уже существует. ");
        $u = new XcmsUser($login);
        $u->set_valid();
        $u->set_param("email", $email);
        $u->set_param("creator", $this->login());
        $u->set_param("creation_date", @time());
        $u->_save();
        return $u;
    }
    /**
      * Удаляет указанного пользователя из системы
      * @param login логин удаляемого пользователя
      **/
    function delete($login)
    {
        $this->check_rights("admin");
        @unlink($this->_file_name($login));
    }
    /**
      * Создает сессию c текущим пользователем
      * TODO: странный API, это какая-то очень private-функция (или название неудачное)
      * @param password пароль пользователя
      **/
    function create_session($password)
    {
        $_SESSION["user"] = $this->login();
        $_SESSION["passwd"] = $this->_hash($this->_hash($password));
    }
    /**
      * Проверяет сессию на соответствие пользователю.
      **/
    function check_session()
    {
        if ($_SESSION["user"] != $this->login())
            throw new Exception("Неправильное имя пользователя. ");
        if ($this->login() == "anonymous")
            return true;

        if (xcms_get_key_or($_SESSION, "passwd") != $this->_hash($this->param("password")))
        {
            $this->_cleanup_session();
            throw new Exception("Неправильный пароль. ", XE_WRONG_PASSWORD);
        }
        return true;
    }
    /**
      * Очищает текущую сессию
      **/
    private function _cleanup_session()
    {
        $_SESSION["user"] = "";
        $_SESSION["passwd"] = "";
    }
    /**
      * Выдаёт список всех пользователей в виде массива логинов
      **/
    function user_list()
    {
        $ans = array();
        $user_files = glob($this->_file_name("*"));
        foreach ($user_files as $li)
        {
            $li = preg_replace('/\\.user$/', "", trim($li));
            $li = preg_replace("/.*\\//", "", $li);
            $ans[] = $li;
        }
        return $ans;
    }
    /**
      * Находит пользователя по email
      * @return login, если нашёлся, и NULL в противном случае
      **/
    function find_by_email($email)
    {
        $users = $this->user_list();
        foreach ($users as $login)
        {
            $dict = xcms_get_list($this->_file_name($login));
            if (xcms_get_key_or($dict, "email") == $email)
                return xcms_get_key_or($dict, "login");
        }
        return NULL;
    }
    /**
      * Операция su (switch user). На самом деле никакой подмены
      * текущего пользователя при этой операции не происходит.
      * @return экземпляр запрошенного пользователя
      **/
    function su($login)
    {
        $this->check_rights("admin");
        return new XcmsUser($login);
    }
    /**
      * Разлогинивает текущего пользователя (в том числе чистит сессию)
      * TODO: не сработает, если вывод уже начался (требуется JS-перенаправление в этом случае)
      * @param redirect URL, на который нужно перенаправить пользователя после выхода
      **/
    function logout($redirect)
    {
        $this->_cleanup_session();
        header("Location: $redirect");
    }
    /**
      * Unit-test для класса XcmsUser
      **/
    static function unit_test()
    {
        xut_begin("XcmsUser");

        $superuser = new XcmsUser("superuser");
        $superuser->set_superuser();
        $superuser->delete("test_user");
        $superuser->create("test_user", "test@example.com");

        xut_check($superuser->add_to_group("test_user", "testGroup1"), "Add to testGroup1");
        xut_check($superuser->add_to_group("test_user", "testGroup2"), "Add to testGroup2");
        xut_check($superuser->add_to_group("test_user", "testGroup3"), "Add to testGroup3");

        $superuser->remove_from_group("test_user", "testGroup2");
        if ($superuser->remove_from_group("test_user", "testGroup2"))
            xut_report("I still can remove user from testGroup2 which he don't belong");

        $user = new XcmsUser("test_user");
        $user->passwd("kuku");
        $user->set_param("name", "Vasya");
        $user->set_param("email", "vasya@example.com");

        try
        {
            $user->set_param("groups", "admin");
            xut_report("User can change his group list");
        } catch (Exception $e) {}

        try
        {
            $user->add_to_group("test_user", "kuku");
            xut_report("User can add himself to group");
        } catch (Exception $e) {}

        $user->check_rights("testGroup1");

        try
        {
            $user->check_rights("testGroup2");
            xut_report("User belong to group it don't belong");
        } catch (Exception $e) {}

        try
        {
            $user->check_rights("testGroup5kuku2");
            xut_report("User belong to undefined group");
        } catch (Exception $e) {}

        $user->create_session("kuku");
        $user->check_session();

        try
        {
            $user->create_session("kuku1");
            $user->check_session();
            xut_report("User can login with invalid password");
        } catch (Exception $e) {}

        if ($superuser->su("test_user")->login() != "test_user")
            xut_report("XcmsUser::su doesn't work properly");

        try
        {
            $superuser->create("another_user", "vasya@example.com");
            xut_report("Able to create another user with same email");
        } catch (Exception $e) {}

        xut_end();
    }
};

/**
  * This one returns current user object. It will have name "anonymous" if no logged in user.
  * If parameter(s) specified, they're pushed to session.
  **/
function xcms_user($login = NULL, $password = NULL)
{
    if ($login != NULL)
        $_SESSION["user"] = $login;
    $login = @$_SESSION["user"];
    if (!strlen($login))
        return new XcmsUser("anonymous");

    $u = new XcmsUser($login);
    if ($password != NULL)
        $u->create_session($password);
    $u->check_session();
    return $u;
}

/**
  * Checks current user access to groups
  * @param $groups groups/users ACL (array)
  * @return true if access granted, false otherwise
  **/
function xcms_check_rights($groups)
{
    $u = xcms_user();
    foreach ($groups as $v)
    {
        if ($v && $v[0] == "#")
        {
            // this is a group
            if ($u->check_rights(substr($v, 1), false))
                return true;
        }
        else
        {
            if ($u->login() == $v)
                return true;
        }
    }
    return false;
}


function xcms_auth_wall_admin()
{
    if (!xcms_user()->check_rights("admin", false))
    {
        die("Impossible to get here. Please report to dev@fizlesh.ru");
    }
}

?>
