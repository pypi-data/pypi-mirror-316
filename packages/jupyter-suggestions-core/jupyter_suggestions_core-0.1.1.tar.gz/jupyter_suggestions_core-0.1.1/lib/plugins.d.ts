import { ISuggestionsManagerRegistry, ISuggestionsModel } from '@jupyter/suggestions-base';
import { JupyterFrontEndPlugin } from '@jupyterlab/application';
export declare const suggestionsModelPlugin: JupyterFrontEndPlugin<ISuggestionsModel>;
export declare const commandsPlugin: JupyterFrontEndPlugin<void>;
export declare const suggestionsPanelPlugin: JupyterFrontEndPlugin<void>;
export declare const suggestionsManagerPlugin: JupyterFrontEndPlugin<void>;
export declare const registryPlugin: JupyterFrontEndPlugin<ISuggestionsManagerRegistry>;
export declare const cellToolbarPlugin: JupyterFrontEndPlugin<void>;
