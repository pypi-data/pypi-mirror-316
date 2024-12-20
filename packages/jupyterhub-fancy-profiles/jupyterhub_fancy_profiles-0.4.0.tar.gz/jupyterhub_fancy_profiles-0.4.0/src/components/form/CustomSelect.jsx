import { useState } from "react";
import Select from "react-select";

/**
 * Customized react-select with a few extra options
 *
 * - Custom renderer to use our CSS classes, so we can theme the description of the
 *   selected item to be readable. This should *probably* be replaced with react-select's
 *   built in theming support eventually
 * - Options now support a title and description, rendered as we would like
 * - Options support 'onSelected' and 'onDeselected' callbacks
 *
 * @typedef {object} Option
 * @property {string} label - User visible label for this option
 * @property {string} value - Value to use for the <input> tag when this option is selected
 * @property {string} [description] - (Optional) description to display under the label
 * @property {} [onSelected] - (Optional) function to be called when this option is selected
 * @property {} [onDeselected] - (Optional) function to be called when this option is deselected
 *
 * @typedef {object} Props - Props to pass to this components. Everything is passed through to React Select
 * @prop {Option[]} options - List of options to display
 *
 * @param {Props} props
 * @returns
 */
export function CustomizedSelect({ options, hasError, ...props }) {
  const [lastSelectedChoice, setLastSelectedChoice] = useState(null);
  return (
    <Select
      options={options}
      formatOptionLabel={(option, meta) => {
        let classNames = ["react-select-item-container"];
        if (meta.selectValue[0].value === option.value) {
          // Check for the values, rather than the whole object, as react-select may make copies
          // We are rendering a value that is the current selection
          classNames.push("react-select-item-selected");
        }
        if (meta.context === "menu") {
          // We are rendering items for display in the menu of options
          classNames.push("react-select-item-menu-display");
        }
        return (
          <div className={classNames.join(" ")}>
            <div className="react-select-item-title">{option.label}</div>
            {option.description && (
              <div className="react-select-item-description">
                {option.description}
              </div>
            )}
          </div>
        );
      }}
      onChange={(option, meta) => {
        console.log(meta);
        if (
          lastSelectedChoice !== null &&
          option !== lastSelectedChoice &&
          lastSelectedChoice.onDeselected
        ) {
          lastSelectedChoice.onDeselected();
        }
        if (option.onSelected) {
          option.onSelected();
        }
        if (props.onChange) {
          props.onChange(option, meta);
        }
        setLastSelectedChoice(option);
      }}
      styles={{
        control: (baseStyles) => ({
          ...baseStyles,
          borderColor: hasError ? "red" : "grey",
        }),
      }}
      {...props}
    />
  );
}
