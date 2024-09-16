export function get_profile() {
    return fetch('/personal/get_profile').then(resp => resp.json())
}
