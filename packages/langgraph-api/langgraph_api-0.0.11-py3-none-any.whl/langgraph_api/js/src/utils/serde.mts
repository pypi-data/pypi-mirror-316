export const serialiseAsDict = (obj: unknown) => {
  return JSON.stringify(
    obj,
    function (key: string | number, value: unknown) {
      const rawValue = this[key];
      if (
        rawValue != null &&
        typeof rawValue === "object" &&
        "toDict" in rawValue &&
        typeof rawValue.toDict === "function"
      ) {
        // TODO: we need to upstream this to LangChainJS
        const { type, data } = rawValue.toDict();
        return { ...data, type };
      }

      return value;
    },
    2
  );
};
