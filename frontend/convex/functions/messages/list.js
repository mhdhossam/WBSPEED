import { query } from "../../_generated/server";

export const list = query(async ({ db }, { limit }) => {
  return await db
    .query("messages")
    .order("desc")
    .take(limit);
});
