import { useTelemetry } from "frappe-ui/frappe";

// Posthog stub — initializes window.posthog if not already present
if (typeof window !== "undefined" && !window.posthog) {
  const e: any = (window.posthog = [] as any);
  e._i = [];
  e.__SV = 1;
  e.init = function () {};
  e.capture = function () {};
  e.identify = function () {};
}

const APP = "helpdesk";

interface CaptureOptions {
  data: {
    [key: string]: string | number | boolean | object;
  };
}

export function capture(event: string, options: CaptureOptions = { data: {} }) {
  const { capture: _capture } = useTelemetry();
  _capture(event, options.data);
}
