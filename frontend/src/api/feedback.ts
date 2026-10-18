import { postJson } from "./http";

export type FeedbackPayload = {
  enjoyment: "gostando" | "neutro" | "nao_gostando";
  comments: string;
  suggestions: string;
};

export function submitFeedback(payload: FeedbackPayload) {
  return postJson("/feedback", payload);
}
