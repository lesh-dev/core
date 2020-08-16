import * as React from "react";

export abstract class ReduxAutofireAction<P = undefined, S = undefined> extends React.Component<P, S> {
    constructor(props: any, ctx: any) {
        super(props, ctx);
        this.reload_do = this.reload_do.bind(this)
        this.reload_schedule();
    }

    reload_schedule() {
        window.setTimeout(this.reload_do, this.reload_interval() * 1000)
    }

    reload_interval() {
        return 60
    }

    reload_should() {
        return true
    }

    private reload_do() {
        if (this.reload_should()) {
            this.reload()
        }
        this.reload_schedule()
    }

    abstract reload(): void
}