import * as React from 'react'

interface ModalProps {
    onClose: () => void
}

export class Modal extends React.Component<ModalProps> {
    constructor(props: ModalProps) {
        super(props)

        this.close = this.close.bind(this)
    }
    private close(e: KeyboardEvent) {
        if (e.key === 'Escape') {
            this.props.onClose()
        }
    }

    componentDidMount(): void {
        document.addEventListener("keydown", this.close)
    }
    componentWillUnmount(): void {
        document.removeEventListener("keydown", this.close)
    }

    render() {
        return <>
            <div
                className="modal"
            >
                {
                    this.props.children
                }
            </div>
            <div
                className="modal__bg"
                onClick={e => this.props.onClose()}
            >
            </div>
        </>
    }
}
