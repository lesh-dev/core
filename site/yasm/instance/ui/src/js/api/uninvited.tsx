export function notification_list(req: number) {
    return fetch('/api/uninvited/' + req).then(resp => resp.json())
}
