/*
 * Shared by the scripts in private/, which esbuild bundles it into. Both throw
 * an error that names what the template no longer renders, where `!` would
 * only give a TypeError on null, or a NaN, further on.
 */

// The first `type` that `selector` finds in `parent`.
export function requiredElement<E extends Element>(
  selector: string,
  type: abstract new () => E,
  parent: ParentNode = document,
): E {
  const element = parent.querySelector(selector);
  if (!(element instanceof type)) {
    throw new TypeError(`The page has no ${type.name} at ${selector}`);
  }
  return element;
}

// The value of the attribute data-* that `key` names in camelCase.
export function requiredData(element: HTMLOrSVGElement, key: string): string {
  const value = element.dataset[key];
  if (value == null) {
    throw new TypeError(`An element has no ${key} in its dataset`);
  }
  return value;
}
