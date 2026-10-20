export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // Route root requests directly to index.html
    if (url.pathname === "/" || url.pathname === "") {
      return env.ASSETS.fetch(new URL("/index.html", request.url));
    }

    // Attempt asset fetch
    const response = await env.ASSETS.fetch(request);

    // Fallback to index.html for extensionless SPA routes
    if (response.status === 404 && !url.pathname.includes(".")) {
      return env.ASSETS.fetch(new URL("/index.html", request.url));
    }

    return response;
  }
};
