export function get_profile() {
    return fetch('/profile/get_profile').then(resp => resp.json())
}
