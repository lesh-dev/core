import * as React from 'react'
import {Link} from "react-router-dom";

export function SRender(domain: string, same: React.ReactNode, other: React.ReactNode): React.ReactNode {
    if (document.location.pathname.startsWith(domain)) {
        return same
    } else {
        return other
    }
}


export function SLink(domain: string, to: string, element: React.ReactNode): React.ReactNode {
    if (document.location.pathname.startsWith(domain)) {
        return (
            <Link to={to}>
                { element }
            </Link>
        )
    } else {
        return (
            <a href={to}>
                { element }
            </a>
        )
    }
}