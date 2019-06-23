export function get_profile() {
    return fetch('/perosnal/get_profile').then(resp => resp.json())
}
