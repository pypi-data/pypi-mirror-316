import { CellToolbarMenu, COMMAND_IDS, hintIcon, ISuggestionsManagerRegistryToken, ISuggestionsModelToken, LocalSuggestionsManager, SuggestionsManagerRegistry, SuggestionsModel, SuggestionsPanelWidget, SuggestionType } from '@jupyter/suggestions-base';
import { ILayoutRestorer } from '@jupyterlab/application';
import { IToolbarWidgetRegistry } from '@jupyterlab/apputils';
import { INotebookTracker } from '@jupyterlab/notebook';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { ITranslator, nullTranslator } from '@jupyterlab/translation';
import { IFormRendererRegistry } from '@jupyterlab/ui-components';
import { SuggestionsSettingComponent } from './settingrenderer';
const NAME_SPACE = '@jupyter/suggestions-core';
export const suggestionsModelPlugin = {
    id: `${NAME_SPACE}:model`,
    description: 'The model of the suggestions panel',
    autoStart: true,
    requires: [INotebookTracker, ISuggestionsManagerRegistryToken],
    provides: ISuggestionsModelToken,
    activate: async (app, tracker, suggestionsManagerRegistry) => {
        console.log(`${NAME_SPACE}:model is activated`);
        const userManager = app.serviceManager.user;
        const suggestionsManager = await suggestionsManagerRegistry.getActivatedManager();
        const model = new SuggestionsModel({
            panel: tracker.currentWidget,
            suggestionsManager,
            userManager
        });
        tracker.currentChanged.connect(async (_, changed) => {
            if (tracker.currentWidget) {
                await tracker.currentWidget.context.ready;
                model.switchNotebook(tracker.currentWidget);
            }
            else {
                model.switchNotebook(null);
            }
        });
        suggestionsManagerRegistry.managerChanged.connect((_, newManager) => {
            model.switchManager(newManager);
        });
        return model;
    }
};
export const commandsPlugin = {
    id: `${NAME_SPACE}:commands`,
    description: 'A JupyterLab extension for suggesting changes.',
    autoStart: true,
    requires: [INotebookTracker, ISuggestionsModelToken],
    optional: [ITranslator],
    activate: (app, tracker, model, translator_) => {
        console.log(`${NAME_SPACE}:commands is activated`);
        const { commands } = app;
        const translator = translator_ !== null && translator_ !== void 0 ? translator_ : nullTranslator;
        const trans = translator.load('jupyterlab');
        commands.addCommand(COMMAND_IDS.addCellSuggestion, {
            caption: trans.__('Add suggestion'),
            execute: async () => {
                const current = tracker.currentWidget;
                if (current !== model.currentNotebookPanel) {
                    await model.switchNotebook(current);
                }
                await model.addSuggestion({ type: SuggestionType.change });
            },
            isVisible: () => true
        });
        commands.addCommand(COMMAND_IDS.addDeleteCellSuggestion, {
            caption: trans.__('Add delete cell suggestion'),
            execute: async () => {
                const current = tracker.currentWidget;
                if (current !== model.currentNotebookPanel) {
                    await model.switchNotebook(current);
                }
                await model.addSuggestion({ type: SuggestionType.delete });
            },
            isVisible: () => true
        });
        tracker.activeCellChanged.connect(() => {
            commands.notifyCommandChanged(COMMAND_IDS.addCellSuggestion);
            commands.notifyCommandChanged(COMMAND_IDS.addDeleteCellSuggestion);
        });
        tracker.selectionChanged.connect(() => {
            commands.notifyCommandChanged(COMMAND_IDS.addCellSuggestion);
            commands.notifyCommandChanged(COMMAND_IDS.addDeleteCellSuggestion);
        });
    }
};
export const suggestionsPanelPlugin = {
    id: `${NAME_SPACE}:panel`,
    description: 'A JupyterLab extension for suggesting changes.',
    autoStart: true,
    requires: [ISuggestionsModelToken, ILayoutRestorer],
    optional: [ITranslator],
    activate: (app, model, restorer, translator_) => {
        console.log(`${NAME_SPACE}:panel is activated`);
        const translator = translator_ !== null && translator_ !== void 0 ? translator_ : nullTranslator;
        const panel = new SuggestionsPanelWidget({ model, translator });
        panel.id = 'jupyter-suggestions:main-panel';
        panel.title.caption = 'Jupyter Suggestions';
        panel.title.icon = hintIcon;
        if (restorer) {
            restorer.add(panel, NAME_SPACE);
        }
        app.shell.add(panel, 'right', { rank: 2000, activate: false });
    }
};
export const suggestionsManagerPlugin = {
    id: `${NAME_SPACE}:manager`,
    description: 'A JupyterLab extension for suggesting changes.',
    autoStart: true,
    requires: [INotebookTracker],
    optional: [ISuggestionsManagerRegistryToken],
    activate: (app, tracker, managerRegistry) => {
        console.log(`${NAME_SPACE}:manager is activated`);
        if (managerRegistry) {
            const manager = new LocalSuggestionsManager({ tracker });
            const success = managerRegistry.register({
                id: 'Local Suggestion Manager',
                manager
            });
            if (!success) {
                console.log('Failed to register the local suggestion manager');
            }
        }
    }
};
export const registryPlugin = {
    id: `${NAME_SPACE}:registry`,
    description: 'Provides the suggestions manager registry.',
    requires: [ISettingRegistry],
    optional: [IFormRendererRegistry, ITranslator],
    provides: ISuggestionsManagerRegistryToken,
    autoStart: true,
    activate: (app, settingRegistry, settingRendererRegistry, translator_) => {
        console.log(`${NAME_SPACE}:registry is activated`);
        const SETTING_KEY = 'suggestionsManager';
        const pluginId = `${NAME_SPACE}:registry`;
        const registryManager = new SuggestionsManagerRegistry();
        const translator = translator_ !== null && translator_ !== void 0 ? translator_ : nullTranslator;
        if (settingRendererRegistry) {
            const renderer = {
                fieldRenderer: (props) => {
                    return SuggestionsSettingComponent({ ...props, translator });
                }
            };
            settingRendererRegistry.addRenderer(`${pluginId}.${SETTING_KEY}`, renderer);
        }
        const updateOptions = async (settings) => {
            const options = settings.composite;
            await registryManager.setManager(options.suggestionsManager);
        };
        settingRegistry.transform(pluginId, {
            fetch: plugin => {
                const schemaProperties = plugin.schema.properties;
                const allManagers = registryManager.getAllManagers();
                if (allManagers.length) {
                    schemaProperties[SETTING_KEY]['availableManagers'] = allManagers;
                }
                return plugin;
            }
        });
        settingRegistry
            .load(pluginId)
            .then(settings => {
            updateOptions(settings);
            settings.changed.connect(() => {
                updateOptions(settings);
            });
        })
            .catch((reason) => {
            console.error(reason);
        });
        registryManager.managerRegistered.connect(() => {
            settingRegistry.load(pluginId, true);
        });
        return registryManager;
    }
};
export const cellToolbarPlugin = {
    id: `${NAME_SPACE}:cell-toolbar`,
    description: 'A JupyterLab extension for suggesting changes.',
    autoStart: true,
    requires: [INotebookTracker, ISuggestionsModelToken],
    optional: [ITranslator, IToolbarWidgetRegistry],
    activate: (app, tracker, model, translator_, toolbarRegistry) => {
        console.log(`${NAME_SPACE}:cell-toolbar is activated`);
        const { commands } = app;
        if (toolbarRegistry) {
            toolbarRegistry.addFactory('Cell', 'jupyter-suggestions-core:cell-suggestion-menu', cell => {
                const w = new CellToolbarMenu({
                    cell,
                    commands,
                    suggestionModel: model
                });
                return w;
            });
        }
    }
};
