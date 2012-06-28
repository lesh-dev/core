<div class="auth-widget">
    <h2>Для данного действия необходима авторизация!</h2>
    <?php
    if (@$auth_noaccess)
    {
        echo $auth_noaccess;
        unset($auth_noaccess);
    }
    else
    {?>
        <div>У вас недостаточно прав для доступа к этому разделу сайта</div>
        <?php
    }
    include("auth_form.php");
    ?>
</div>
