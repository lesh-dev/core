import { call } from "../axios";
import { PatchAction } from "./common";

export type ContactsPatch = Map<string, {
    name: string,
    action: PatchAction,
}>


export function setAva(avaSrc: string) {
    return call(
        '/i/api/set_ava',
        {
            new_ava: avaSrc,
        }
    )
}

export function patchContacts(patch: ContactsPatch) {
    const p = {} as {[index: string]: {name: string, action: PatchAction}}
    for (const e of patch.entries()) {
        p[e[0]] = {
            name: e[1].name,
            action: e[1].action,
        }
    }
    return call(
        '/i/api/patch_contacts',
        {
            patch: p,
        }
    )
}