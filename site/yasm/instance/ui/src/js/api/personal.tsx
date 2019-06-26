export function get_profile() {
    return fetch('/internal/get_profile').then(resp => resp.json())
}
