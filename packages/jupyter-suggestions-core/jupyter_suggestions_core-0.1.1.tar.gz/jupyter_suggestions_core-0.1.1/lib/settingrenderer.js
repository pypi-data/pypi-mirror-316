import React, { useCallback, useEffect, useMemo, useState } from 'react';
const SETTING_NAME = 'suggestionsManager';
/**
 * Custom setting renderer for suggestion extension extension.
 */
export function SuggestionsSettingComponent(props) {
    const { formContext, schema } = props;
    const settings = useMemo(() => formContext.settings, [formContext.settings]);
    const selectedValue = useMemo(() => {
        var _a, _b;
        return ((_b = (_a = settings === null || settings === void 0 ? void 0 : settings.composite) === null || _a === void 0 ? void 0 : _a[SETTING_NAME]) !== null && _b !== void 0 ? _b : 'None');
    }, [settings === null || settings === void 0 ? void 0 : settings.composite]);
    useEffect(() => {
        setState(selectedValue);
    }, [selectedValue]);
    const [state, setState] = useState(selectedValue);
    const allOptions = useMemo(() => {
        const allManagers = schema['availableManagers'];
        return [...allManagers].map(it => ({ value: it, label: it }));
    }, [schema]);
    const onChange = useCallback((value) => {
        settings === null || settings === void 0 ? void 0 : settings.set(SETTING_NAME, value);
        setState(value);
    }, [settings]);
    return (React.createElement("div", { className: "jp-inputFieldWrapper jp-FormGroup-contentItem" },
        React.createElement("select", { className: "form-control", value: state, onChange: e => onChange(e.target.value) }, allOptions.map((it, idx) => (React.createElement("option", { key: idx, value: it.value }, it.label))))));
}
