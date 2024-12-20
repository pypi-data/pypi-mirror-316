import { ITranslator } from '@jupyterlab/translation';
import type { FieldProps } from '@rjsf/utils';
interface IProps extends FieldProps {
    translator: ITranslator;
}
/**
 * Custom setting renderer for suggestion extension extension.
 */
export declare function SuggestionsSettingComponent(props: IProps): JSX.Element;
export {};
