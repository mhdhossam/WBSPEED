import { httpRouter } from "convex/server";
import { httpAction } from "./_generated/server";
import { api } from "./_generated/api";

const http = httpRouter();

/* LIST */
http.route({
  path: "/messages/list",
  method: "POST",
  handler: httpAction(async (ctx, req) => {
    const body = await req.json();

    const result = await ctx.runQuery(api.messages.list, body);

    return new Response(JSON.stringify(result), {
      headers: { "Content-Type": "application/json" },
    });
  }),
});

/* ADD */
http.route({
  path: "/messages/add",
  method: "POST",
  handler: httpAction(async (ctx, req) => {
    const body = await req.json();

    const result = await ctx.runMutation(api.messages.add, body);

    return new Response(JSON.stringify(result), {
      headers: { "Content-Type": "application/json" },
    });
  }),
});

export default http;
