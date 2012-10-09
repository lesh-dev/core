<?php
    class XcmsUser
    {
        /*var $dict = array();
        var $error = "";
        var $superuser = false;*/
        private function _file_name($login)
        {
            global $SETTINGS, $content_dir;
            $cd = $SETTINGS["datadir"];
            if($cd == "") $cd = $content_dir;
            if($cd == "")
                throw new Exception ("Content dir is empty!");
            return "$cd/auth/usr/$login.user";
        }
        private function _hash($string)
        {
            return md5($string."saulty!");
        }
        /**
          * Сериализует пользователя
          **/
        private function _save()
        {
            if(!$this->valid)
                throw new Exception("Cannot save invalid user!");

            if(!$this->isNull())
                xcms_save_list($this->_file_name($this->login()),$this->dict);
            else return $this->setError("User is NULL, can't serialize!");
            return true;
        }
        function isValid()
        {
            return $this->valid;
        }
        function setValid()
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
            $this->isSuperuser = false;
        }
        /**
          * Возвращает текущее имя пользователя
          **/
        function login()
        {
            return $this->dict["login"];
        }

        function setParam($key, $value) /// Ooops. This was qt-style naming, will remove later.
        {
            return $this->set_param($key,$value);
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
            return explode(",",@$this->dict["groups"]);
        }
        function check_rights($group, $throw_exception=true)
        {
            $group = str_replace("#","",$group);
            if($group == "all") return true;
            if($group == "registered" && $this->isValid()) return true;
            if($this->isSuperuser()) return true;
            if(in_array($group,$this->groups())) return true;
            if($throw_exception)
                throw new Exception("User don't belong to group $group to perform this action");
            return false;
        }
        /**
          * Возвращает true, если пользователь кривой.
          **/
        function isNull()
        {
            if(strlen($this->login()))
                return false;
            return true;
        }
        /**
          * Обнуляет пользователя
          **/
        function setNull()
        {
            $this->check_rights("admin");
            $this->dict = array();
        }
        /**
          * Делает пользователя суперпользователем, для которого любые проверки прав успешны.
          **/
        function setSuperuser()
        {
            // This is only way to get SU flag from code!
            $this->isSuperuser = true;
        }
        /**
          * Указывает, является ли пользователь суперпользователем.
          **/
        function isSuperuser()
        {
            return $this->isSuperuser;
        }
        /**
          * Добавляет пользователя в группу.
          **/
        function group_add($login, $group)
        {
            $group = str_replace("#","",$group);
            $this->check_rights("admin");
            $user = new XcmsUser($login);
            if(in_array($group,$user->groups()))
                return $this->setError("User already presented in this group");
            $user->dict["groups"] = implode(",",array_merge($user->groups(), array($group)));
            $user->_save();
        }
        function group_remove($login, $group)
        {
            $group = str_replace("#","",$group);
            $this->check_rights("admin");
            $user = new XcmsUser($login);
            if(!in_array($group,$user->groups()))
                return $this->setError("User does not belong to this group!");
            $user->dict["groups"] = implode(",",array_diff($user->groups(), array($group)));
            $user->_save();
        }
        /**
          * Выставляет значение lastError
          **/
        function setError($error)
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
          **/
        function passwd($password)
        {
            $this->dict["password"] = $this->_hash($password);
            $this->plaintext_password = $password;
            $this->_save();
        }
        /**
          * Создает нового пользователя
          **/
        function create($login, $email="nobody@example.com")
        {
            if(preg_replace("/[a-zA-Z0-9@._-]+/i","",$login) != "")
                throw new Exception("Login format is incorrect!");
            $this->check_rights("admin");
            if(file_exists($this->_file_name($login)))
                return $this->setError("User $login already exists!");
            $u = new XcmsUser($login);
            $u->setValid();
            $u->setParam("email",$email);
            $u->set_param("creator",$this->login());
            $u->set_param("creation_date",@mktime());
            $u->_save();
            return $u;
        }
        /**
          * Удаляет пользователя из системы
          **/
        function delete($login)
        {
            $this->check_rights("admin");
            @unlink($this->_file_name($login));
        }
        /**
          * Создает сессию c текущим пользователем.
          **/
        function create_session($password)
        {
            global $_SESSION;
            $_SESSION["user"] = $this->login();
            $_SESSION["passwd"] = $this->_hash($this->_hash($password));
        }
        /**
          * Проверяет сессию на соответствие пользователю.
          **/
        function check_session()
        {
            global $_SESSION;
            if($_SESSION["user"] != $this->login())
                throw new Exception("Wrong username!");
            if($this->login() == "anonymous")
                return true;

            if($_SESSION["passwd"] != $this->_hash($this->param("password")))
                throw new Exception("Wrong password!");
            return true;
        }
        function user_list()
        {
            $ans = array();
            foreach(glob($this->_file_name("*")) as $li)
            {
                $li = preg_replace("/\\.user/","",$li);
                $li = preg_replace("/.*\\//","",$li);
                $ans[] = $li;
            }
            return $ans;
        }
        function su($login)
        {
            $this->check_rights("admin");
            return new XcmsUser($login);
        }
        /**
          * Unit-test для класса XcmsUser
          **/
        static function unit_test()
        {
            $superuser = new XcmsUser("superuser");
            $superuser->setSuperuser();
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
            $user->setParam("name","Vasya");
            $user->setParam("email","vasya@example.com");

            try{
                $user->setParam("groups","admin");
            echo("Unit test failed: user can change his group list"); } catch (Exception $e) {}

            try{
                $user->group_add("test_user","kuku");
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
        function logout($redirect)
        {
            $_SESSION["user"] = "";
            $_SESSION["passwd"] = "";
            header("Location: $redirect");
        }
    };
    /**
      * This one returns current user object. It will have name "anonymous" if no logged in user.
      * If parameter(s) specified, they're pushed to session.
      **/
    function xcms_user($login = NULL, $password= NULL)
    {
        global $_SESSION;
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
