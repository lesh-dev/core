<?php
    // error codes for generic errors
    define('XE_WRONG_PASSWORD',       1000);
    define('XE_ACCESS_DENIED',        1001);

    class XcmsUser
    {
        private function _file_name($login)
        {
            global $SETTINGS, $content_dir;
            $cd = $SETTINGS["datadir"];
            if (empty($cd)) $cd = $content_dir;
            if (empty($cd))
                throw new Exception ("Content directory not set in SETTINGS. ");
            return "$cd/auth/usr/$login.user";
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
            if(!$this->is_valid())
                throw new Exception("Cannot save invalid user. ");

            if(!$this->is_null())
                xcms_save_list($this->_file_name($this->login()), $this->dict);
            else return $this->set_error("User is NULL, can't serialize!");
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
            if(file_exists($fn))
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
            if(!in_array($key, array("password","email","name", "creator", "creation_date")))
                $this->check_rights("admin");
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
            return explode(",", @$this->dict["groups"]);
        }
        function check_rights($group, $throw_exception=true)
        {
            $group = str_replace("#","",$group);
            if($group == "all") return true;
            if($group == "registered" && $this->is_valid()) return true;
            if($this->is_superuser()) return true;
            if(in_array($group,$this->groups())) return true;
            if($throw_exception)
                throw new Exception("User doesn't belong to group $group to perform this action");
            return false;
        }
        /**
          * Возвращает true, если пользователь кривой.
          **/
        function is_null()
        {
            if(strlen($this->login()))
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
          * TODO: переименовать в add_to_group
          **/
        function group_add($login, $group)
        {
            $group = str_replace("#","",$group);
            $this->check_rights("admin");
            $user = new XcmsUser($login);
            if(in_array($group,$user->groups()))
                return $this->set_error("User already presented in this group");
            $user->dict["groups"] = implode(",", array_merge($user->groups(), array($group)));
            $user->_save();
        }
        /**
          * Удаляет пользователя из группы
          * TODO: переименовать в remove_from_group
          **/
        function group_remove($login, $group)
        {
            $group = str_replace("#","",$group);
            $this->check_rights("admin");
            $user = new XcmsUser($login);
            if(!in_array($group,$user->groups()))
                return $this->set_error("User does not belong to this group!");
            $user->dict["groups"] = implode(",",array_diff($user->groups(), array($group)));
            $user->_save();
        }
        /**
          * Выставляет значение последней ошибки
          **/
        function set_error($error)
        {
            $this->error = $error;
            throw new Exception($error);
            return $error;
        }
        /**
          * Возвращает последнюю ошибку
          **/
        function error()
        {
            return $this->error;
        }
        /**
          * Задает новый пароль пользователю
          * TODO: Зачем хранить plaintext_password? Очень непонятное поведение,
          * скорее всего небезопасное.
          **/
        function passwd($password)
        {
            if (!xcms_check_password($password))
                throw new Exception("Password contains invalid characters. ");
            $this->dict["password"] = $this->_hash($password);
            $this->plaintext_password = $password;
            $this->_save();
        }
        /**
          * Создает нового пользователя
          * @param login логин нового пользователя
          * @param email email нового пользователя (не обязательно)
          * @return экземпляр созданного только что пользователя
          **/
        function create($login, $email = "nobody@example.com")
        {
            if (!xcms_check_user_name($login))
                throw new Exception("Login format is incorrect. ");
            $this->check_rights("admin");
            if(file_exists($this->_file_name($login)))
                return $this->set_error("User $login already exists. ");
            $u = new XcmsUser($login);
            $u->set_valid();
            $u->set_param("email", $email);
            $u->set_param("creator", $this->login());
            $u->set_param("creation_date", @mktime());
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
            if($_SESSION["user"] != $this->login())
                throw new Exception("Неправильное имя пользователя. ");
            if($this->login() == "anonymous")
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
            foreach(glob($this->_file_name("*")) as $li)
            {
                $li = preg_replace("/\\.user/", "", $li);
                $li = preg_replace("/.*\\//", "", $li);
                $ans[] = $li;
            }
            return $ans;
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
            $superuser = new XcmsUser("superuser");
            $superuser->set_superuser();
            $superuser->delete("test_user");
            $superuser->create("test_user", "test@example.com");
            $superuser->group_add("test_user", "testGroup1");
            $superuser->group_add("test_user", "testGroup2");
            $superuser->group_add("test_user", "testGroup3");
            $superuser->group_remove("test_user", "testGroup2");
            try
            {
                $superuser->group_remove("test_user", "testGroup2");
                echo ("Unit test failed: I still can remove user from testGroup2 which he don't belong");
            }
            catch (Exception $e)
            {
                // it's OK to fail here.
            }

            $user = new XcmsUser("test_user");
            $user->passwd("kuku");
            $user->set_param("name", "Vasya");
            $user->set_param("email", "vasya@example.com");

            try{
                $user->set_param("groups", "admin");
            echo("Unit test failed: user can change his group list"); } catch (Exception $e) {}

            try{
                $user->group_add("test_user", "kuku");
            echo("Unit test failed: user can add himself to group"); } catch (Exception $e) {}

            $user->check_rights("testGroup1");

            try{
                $user->check_rights("testGroup2");
            echo ("User belong to group it don't belong"); } catch (Exception $e) {}
            try{
                $user->check_rights("testGroup5kuku2");
            echo("User belong to undefined group"); } catch (Exception $e) {}

            $user->create_session("kuku");
            $user->check_session();

            try{
                $user->create_session("kuku1");
                $user->check_session();
            echo("User can login with invalid password"); } catch (Exception $e) {}

            if($superuser->su("test_user")->login() != "test_user")
                throw new Exception("su don't work");
        }
    };
    /**
      * This one returns current user object. It will have name "anonymous" if no logged in user.
      * If parameter(s) specified, they're pushed to session.
      **/
    function xcms_user($login = NULL, $password= NULL)
    {
        if($login != NULL)
            $_SESSION["user"] = $login;
        $login = @$_SESSION["user"];
        //echo "<h3>$login ";
        if(!strlen($login))
        {
            return new XcmsUser("anonymous");
        }
        $u = new XcmsUser($login);
        if($password != NULL)
            $u->create_session($password);
        $u->check_session();
        return $u;
    }
?>
