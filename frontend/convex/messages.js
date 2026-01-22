import { query, mutation } from "./_generated/server";
import { v } from "convex/values";

export const list = query({
  args: { limit: v.number() },
  handler: async ({ db }, { limit }) => {
    return await db
      .query("messages")
      .order("desc")
      .take(limit);
  },
});

export const add = mutation({
  args: { content: v.string() },
  handler: async ({ db }, { content }) => {
    return await db.insert("messages", {
      content,
      createdAt: Date.now(),
    });
  },
});
