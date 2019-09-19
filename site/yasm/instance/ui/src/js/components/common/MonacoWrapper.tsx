import * as React from 'react'

import * as monacoEditor from 'monaco-editor/esm/vs/editor/editor.api'
import MonacoEditor, {MonacoEditorProps} from 'react-monaco-editor'

interface MonacoWrapperProps extends MonacoEditorProps {
    onDidChangeModelContent?: (e: monacoEditor.editor.IModelContentChangedEvent) => void,

    onDidChangeModelLanguage?: (e: monacoEditor.editor.IModelLanguageChangedEvent) => void,

    onDidChangeModelLanguageConfiguration?: (e: monacoEditor.editor.IModelLanguageConfigurationChangedEvent) => void,

    onDidChangeModelOptions?: (e: monacoEditor.editor.IModelOptionsChangedEvent) => void,

    onDidChangeConfiguration?: (e: monacoEditor.editor.IConfigurationChangedEvent) => void,

    onDidChangeCursorPosition?: (e: monacoEditor.editor.ICursorPositionChangedEvent) => void,

    onDidChangeCursorSelection?: (e: monacoEditor.editor.ICursorSelectionChangedEvent) => void,

    onDidChangeModel?: (e: monacoEditor.editor.IModelChangedEvent) => void,

    onDidChangeModelDecorations?: (e: monacoEditor.editor.IModelDecorationsChangedEvent) => void,

    onDidFocusEditorText?: () => void,

    onDidBlurEditorText?: () => void,

    onDidFocusEditorWidget?: () => void,

    onDidBlurEditorWidget?: () => void,

    onCompositionStart?: () => void,

    onCompositionEnd?: () => void,

    onMouseUp?: (e: monacoEditor.editor.IEditorMouseEvent) => void,

    onMouseDown?: (e: monacoEditor.editor.IEditorMouseEvent) => void,

    onContextMenu?: (e: monacoEditor.editor.IEditorMouseEvent) => void,

    onMouseMove?: (e: monacoEditor.editor.IEditorMouseEvent) => void,

    onMouseLeave?: (e: monacoEditor.editor.IPartialEditorMouseEvent) => void,

    onKeyUp?: (e: monacoEditor.IKeyboardEvent) => void,

    onKeyDown?: (e: monacoEditor.IKeyboardEvent) => void,

    onDidLayoutChange?: (e: monacoEditor.editor.EditorLayoutInfo) => void,

    onDidScrollChange?: (e: monacoEditor.IScrollEvent) => void,
}

interface MonacoWrapperState {
    editor: monacoEditor.editor.IStandaloneCodeEditor,
}

export class MonacoWrapper extends React.Component<MonacoWrapperProps, MonacoWrapperState> {
    constructor(props?: MonacoWrapperProps) {
        super(props);
        this.state = {
            editor: undefined
        }
    }

    onEditorMount(editor?: monacoEditor.editor.IStandaloneCodeEditor) {
        this.setState({editor})
        if (this.props.onDidChangeCursorSelection) {
            editor.onDidChangeCursorSelection(this.props.onDidChangeCursorSelection)
        }

        if (this.props.onDidChangeModelContent) {
            editor.onDidChangeModelContent(this.props.onDidChangeModelContent)
        }

        if (this.props.onDidChangeModelLanguage) {
            editor.onDidChangeModelLanguage(this.props.onDidChangeModelLanguage)
        }

        if (this.props.onDidChangeModelLanguageConfiguration) {
            editor.onDidChangeModelLanguageConfiguration(this.props.onDidChangeModelLanguageConfiguration)
        }

        if (this.props.onDidChangeModelOptions) {
            editor.onDidChangeModelOptions(this.props.onDidChangeModelOptions)
        }

        if (this.props.onDidChangeConfiguration) {
            editor.onDidChangeConfiguration(this.props.onDidChangeConfiguration)
        }

        if (this.props.onDidChangeCursorPosition) {
            editor.onDidChangeCursorPosition(this.props.onDidChangeCursorPosition)
        }

        if (this.props.onDidChangeCursorSelection) {
            editor.onDidChangeCursorSelection(this.props.onDidChangeCursorSelection)
        }

        if (this.props.onDidChangeModel) {
            editor.onDidChangeModel(this.props.onDidChangeModel)
        }

        if (this.props.onDidChangeModelDecorations) {
            editor.onDidChangeModelDecorations(this.props.onDidChangeModelDecorations)
        }

        if (this.props.onDidFocusEditorText) {
            editor.onDidFocusEditorText(this.props.onDidFocusEditorText)
        }

        if (this.props.onDidBlurEditorText) {
            editor.onDidBlurEditorText(this.props.onDidBlurEditorText)
        }

        if (this.props.onDidFocusEditorWidget) {
            editor.onDidFocusEditorWidget(this.props.onDidFocusEditorWidget)
        }

        if (this.props.onDidBlurEditorWidget) {
            editor.onDidBlurEditorWidget(this.props.onDidBlurEditorWidget)
        }

        if (this.props.onCompositionStart) {
            editor.onCompositionStart(this.props.onCompositionStart)
        }

        if (this.props.onCompositionEnd) {
            editor.onCompositionEnd(this.props.onCompositionEnd)
        }

        if (this.props.onMouseUp) {
            editor.onMouseUp(this.props.onMouseUp)
        }

        if (this.props.onMouseDown) {
            editor.onMouseDown(this.props.onMouseDown)
        }

        if (this.props.onContextMenu) {
            editor.onContextMenu(this.props.onContextMenu)
        }

        if (this.props.onMouseMove) {
            editor.onMouseMove(this.props.onMouseMove)
        }

        if (this.props.onMouseLeave) {
            editor.onMouseLeave(this.props.onMouseLeave)
        }

        if (this.props.onKeyUp) {
            editor.onKeyUp(this.props.onKeyUp)
        }

        if (this.props.onKeyDown) {
            editor.onKeyDown(this.props.onKeyDown)
        }

        if (this.props.onDidLayoutChange) {
            editor.onDidLayoutChange(this.props.onDidLayoutChange)
        }

        if (this.props.onDidScrollChange) {
            editor.onDidScrollChange(this.props.onDidScrollChange)
        }
    }

    render() {
        return (
            <MonacoEditor
                {...this.props}
                editorDidMount={editor => this.onEditorMount(editor)}
            />
        )
    }
}
