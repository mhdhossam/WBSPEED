import { mutation } from "../../_generated/server";

export const add = mutation(async ({ db }, { content }) => {
  await db.insert("messages", {
    content,
    createdAt: Date.now(),
  });
});
