export interface Match<T> {
    params: T,
    path: string,
    url: string,
    exact: boolean,
}

export interface RouterProps<T> {
    match?: Match<T>,
}