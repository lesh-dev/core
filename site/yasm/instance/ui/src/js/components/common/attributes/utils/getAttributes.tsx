import * as nm from "normalizr"

type Person = { person_id: number, first_name: string, last_name: string }
type Attr = { person_school_id: number, field: string, value: string }
type AttributeResponseItem = { person_school_id: number, person: Person, person_attributes: Attr[], calendar: Attr[] }

function normalizeAttributes(resp: AttributeResponseItem[]) {
    function reshapeAttrs(attrs: Attr[]) {
        return Object.assign({}, ...attrs.map(a => ({ [a.field]: a.value })) );
    }
    function reshapeCalendar(attrs: any[]) { // FIXME
        return Object.assign({}, ...attrs.map(a => ({ [a.data]: a.status })) );
    }
    function reshapeItem(item: AttributeResponseItem) {
        const {person_attributes, calendar, ...rest} = item;
        return {person_attributes: reshapeAttrs(person_attributes), calendar: reshapeCalendar(calendar), ...rest};
    }
    const reshaped = resp.map(reshapeItem);

    const person = new nm.schema.Entity('persons', {}, {idAttribute: 'person_id'});
    const person_school = new nm.schema.Entity('person_schools', {person}, {idAttribute: 'person_school_id'});
    const {entities, result} = nm.normalize(reshaped, [person_school]);
    return {entities, result};
}


const getAttributes = (school_id: number) => fetch(`
    /postgrest/person_school?
    select=person_school_id,person(*),person_attributes(*),calendar(*)
    &school_id=eq.${school_id}
    `.replace(/ +/g, ''))
    .then(resp => resp.json())
    .then(normalizeAttributes)

export default getAttributes;