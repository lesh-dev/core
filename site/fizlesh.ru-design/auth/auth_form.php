<style>
    div.auth-widget {
        border: 1px solid #7f7f7f;
        border-radius: 3px;
        margin-top: 10px;
        margin-bottom: 10px;
        padding-left: 5px;
        padding-right: 5px;
        padding-bottom: 3px;
        width: 600px;
        background-color: #dddcae;
    }
    input {
        border: 1px solid #7f7f7f;
        padding-left: 2px;
        padding-right: 2px;
    }
    input[type="submit"] {
        border: 2px solid #7f7f7f;
        border-radius: 2px;
        padding-left: 5px;
        padding-right: 5px;
        min-width: 70px;
    }

</style>

<form method="post">
<table>
    <tr>
        <td>Логин</td>
        <td><input type="text" name="auth-login" /></td>
    </tr>
    <tr>
        <td>Пароль:</td>
        <td><input type="password" name="auth-passw" /></td>
    </tr>
</table>
<input type="submit" value="Войти" />
</form>