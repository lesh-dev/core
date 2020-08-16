import {Ava, Person} from "../generated/frontend/interfaces/yasm/database";

interface AvaTuple {
    latest: Ava
    other: Ava[]
}

export function split_avas(person: Person): AvaTuple {
    if (person.avas === undefined || person.avas === null) {
        return {latest: null, other: []}
    } else {
        let latest: Ava = null
        const other: Ava[] = []
        for (const ava of person.avas) {
            if (latest === null) {
                latest = ava
            } else {
                if (ava.timestamp > latest.timestamp) {
                    other.push(latest)
                    latest = ava
                } else {
                    other.push(ava)
                }
            }
        }
        other.sort((a, b) => (new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()))
        return {latest, other}
    }
}