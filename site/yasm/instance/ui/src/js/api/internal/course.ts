import {Person} from "../../generated/interfaces";
import {PatchAction} from "./common";
import {call} from "../axios";

export type CourseTeacherPatch = Map<number, {
    value: Person,
    action: PatchAction,
}>

export function patchTeachers(id: number, patch: CourseTeacherPatch) {
    const p = {} as {[index: number]: {action: PatchAction}}
    for (const e of patch.entries()) {
        p[e[0]] = {
            action: e[1].action,
        }
    }
    return call(
        '/i/api/patch_teachers',
        {
            id,
            patch: p,
        }
    )
}