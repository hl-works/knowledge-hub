import '@astrojs/internal-helpers/path';
import '@astrojs/internal-helpers/remote';
import 'piccolore';
import { N as NOOP_MIDDLEWARE_HEADER, i as decodeKey } from './chunks/astro/server_CeIjrliP.mjs';
import 'clsx';
import 'es-module-lexer';
import 'html-escaper';

const NOOP_MIDDLEWARE_FN = async (_ctx, next) => {
  const response = await next();
  response.headers.set(NOOP_MIDDLEWARE_HEADER, "true");
  return response;
};

const codeToStatusMap = {
  // Implemented from IANA HTTP Status Code Registry
  // https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  PAYMENT_REQUIRED: 402,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  METHOD_NOT_ALLOWED: 405,
  NOT_ACCEPTABLE: 406,
  PROXY_AUTHENTICATION_REQUIRED: 407,
  REQUEST_TIMEOUT: 408,
  CONFLICT: 409,
  GONE: 410,
  LENGTH_REQUIRED: 411,
  PRECONDITION_FAILED: 412,
  CONTENT_TOO_LARGE: 413,
  URI_TOO_LONG: 414,
  UNSUPPORTED_MEDIA_TYPE: 415,
  RANGE_NOT_SATISFIABLE: 416,
  EXPECTATION_FAILED: 417,
  MISDIRECTED_REQUEST: 421,
  UNPROCESSABLE_CONTENT: 422,
  LOCKED: 423,
  FAILED_DEPENDENCY: 424,
  TOO_EARLY: 425,
  UPGRADE_REQUIRED: 426,
  PRECONDITION_REQUIRED: 428,
  TOO_MANY_REQUESTS: 429,
  REQUEST_HEADER_FIELDS_TOO_LARGE: 431,
  UNAVAILABLE_FOR_LEGAL_REASONS: 451,
  INTERNAL_SERVER_ERROR: 500,
  NOT_IMPLEMENTED: 501,
  BAD_GATEWAY: 502,
  SERVICE_UNAVAILABLE: 503,
  GATEWAY_TIMEOUT: 504,
  HTTP_VERSION_NOT_SUPPORTED: 505,
  VARIANT_ALSO_NEGOTIATES: 506,
  INSUFFICIENT_STORAGE: 507,
  LOOP_DETECTED: 508,
  NETWORK_AUTHENTICATION_REQUIRED: 511
};
Object.entries(codeToStatusMap).reduce(
  // reverse the key-value pairs
  (acc, [key, value]) => ({ ...acc, [value]: key }),
  {}
);

function sanitizeParams(params) {
  return Object.fromEntries(
    Object.entries(params).map(([key, value]) => {
      if (typeof value === "string") {
        return [key, value.normalize().replace(/#/g, "%23").replace(/\?/g, "%3F")];
      }
      return [key, value];
    })
  );
}
function getParameter(part, params) {
  if (part.spread) {
    return params[part.content.slice(3)] || "";
  }
  if (part.dynamic) {
    if (!params[part.content]) {
      throw new TypeError(`Missing parameter: ${part.content}`);
    }
    return params[part.content];
  }
  return part.content.normalize().replace(/\?/g, "%3F").replace(/#/g, "%23").replace(/%5B/g, "[").replace(/%5D/g, "]");
}
function getSegment(segment, params) {
  const segmentPath = segment.map((part) => getParameter(part, params)).join("");
  return segmentPath ? "/" + segmentPath : "";
}
function getRouteGenerator(segments, addTrailingSlash) {
  return (params) => {
    const sanitizedParams = sanitizeParams(params);
    let trailing = "";
    if (addTrailingSlash === "always" && segments.length) {
      trailing = "/";
    }
    const path = segments.map((segment) => getSegment(segment, sanitizedParams)).join("") + trailing;
    return path || "/";
  };
}

function deserializeRouteData(rawRouteData) {
  return {
    route: rawRouteData.route,
    type: rawRouteData.type,
    pattern: new RegExp(rawRouteData.pattern),
    params: rawRouteData.params,
    component: rawRouteData.component,
    generate: getRouteGenerator(rawRouteData.segments, rawRouteData._meta.trailingSlash),
    pathname: rawRouteData.pathname || void 0,
    segments: rawRouteData.segments,
    prerender: rawRouteData.prerender,
    redirect: rawRouteData.redirect,
    redirectRoute: rawRouteData.redirectRoute ? deserializeRouteData(rawRouteData.redirectRoute) : void 0,
    fallbackRoutes: rawRouteData.fallbackRoutes.map((fallback) => {
      return deserializeRouteData(fallback);
    }),
    isIndex: rawRouteData.isIndex,
    origin: rawRouteData.origin
  };
}

function deserializeManifest(serializedManifest) {
  const routes = [];
  for (const serializedRoute of serializedManifest.routes) {
    routes.push({
      ...serializedRoute,
      routeData: deserializeRouteData(serializedRoute.routeData)
    });
    const route = serializedRoute;
    route.routeData = deserializeRouteData(serializedRoute.routeData);
  }
  const assets = new Set(serializedManifest.assets);
  const componentMetadata = new Map(serializedManifest.componentMetadata);
  const inlinedScripts = new Map(serializedManifest.inlinedScripts);
  const clientDirectives = new Map(serializedManifest.clientDirectives);
  const serverIslandNameMap = new Map(serializedManifest.serverIslandNameMap);
  const key = decodeKey(serializedManifest.key);
  return {
    // in case user middleware exists, this no-op middleware will be reassigned (see plugin-ssr.ts)
    middleware() {
      return { onRequest: NOOP_MIDDLEWARE_FN };
    },
    ...serializedManifest,
    assets,
    componentMetadata,
    inlinedScripts,
    clientDirectives,
    routes,
    serverIslandNameMap,
    key
  };
}

const manifest = deserializeManifest({"hrefRoot":"file:///home/user/knowledge-hub/atlas-asie-app/","cacheDir":"file:///home/user/knowledge-hub/atlas-asie-app/node_modules/.astro/","outDir":"file:///home/user/knowledge-hub/atlas-asie/","srcDir":"file:///home/user/knowledge-hub/atlas-asie-app/src/","publicDir":"file:///home/user/knowledge-hub/atlas-asie-app/public/","buildClientDir":"file:///home/user/knowledge-hub/atlas-asie/client/","buildServerDir":"file:///home/user/knowledge-hub/atlas-asie/server/","adapterName":"","routes":[{"file":"file:///home/user/knowledge-hub/atlas-asie/carnet/index.html","links":[],"scripts":[],"styles":[{"type":"external","src":"/atlas-asie/_astro/carnet.DqrDj1-l.css"},{"type":"inline","content":".intro{padding:clamp(30px,6vw,64px) 0 clamp(6px,2vw,18px)}.intro h1{font-size:clamp(2.6rem,8vw,5rem);margin:0 0 .6rem}.feed{padding:clamp(16px,3vw,32px) 0 clamp(40px,6vw,80px)}.empty{border:2px dashed var(--line);border-radius:var(--r);background:var(--card);padding:clamp(30px,6vw,60px);text-align:center;max-width:60ch;margin:0 auto}.empty .ig{display:inline-grid;place-items:center;width:64px;height:64px;border-radius:16px;background:linear-gradient(135deg,var(--orange),var(--yellow));color:#fff;margin-bottom:14px}.empty h2{font-family:var(--disp);text-transform:uppercase;font-size:1.6rem;margin:0 0 .5rem}.empty p{color:var(--ink-soft);margin:.4rem 0}.empty .note{font-size:.86rem;color:var(--muted);margin-top:1rem}\n"}],"routeData":{"route":"/carnet","isIndex":false,"type":"page","pattern":"^\\/carnet\\/?$","segments":[[{"content":"carnet","dynamic":false,"spread":false}]],"params":[],"component":"src/pages/carnet.astro","pathname":"/carnet","prerender":true,"fallbackRoutes":[],"distURL":[],"origin":"project","_meta":{"trailingSlash":"ignore"}}},{"file":"file:///home/user/knowledge-hub/atlas-asie/galerie/index.html","links":[],"scripts":[],"styles":[{"type":"external","src":"/atlas-asie/_astro/carnet.DqrDj1-l.css"},{"type":"inline","content":".intro{padding:clamp(30px,6vw,64px) 0 clamp(6px,2vw,18px)}.intro h1{font-size:clamp(2.6rem,8vw,5rem);margin:0 0 .6rem}.gal{padding:clamp(16px,3vw,32px) 0 clamp(40px,6vw,80px)}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px}.grid figure{margin:0;position:relative;border:2px solid var(--ink);border-radius:12px;overflow:hidden;cursor:zoom-in;aspect-ratio:4/3;box-shadow:var(--shadow)}.grid img{width:100%;height:100%;object-fit:cover;transition:transform .3s ease}.grid figure:hover img{transform:scale(1.05)}.grid figcaption{position:absolute;left:0;right:0;bottom:0;padding:8px 10px;font-size:.78rem;font-weight:600;color:#fff;background:linear-gradient(transparent,#140c08bf)}.empty{border:2px dashed var(--line);border-radius:var(--r);background:var(--card);padding:clamp(30px,6vw,60px);text-align:center;max-width:56ch;margin:0 auto;color:var(--ink-soft)}.empty h2{font-family:var(--disp);text-transform:uppercase;font-size:1.5rem;margin:0 0 .5rem;color:var(--ink)}.loading{color:var(--muted)}.lb{position:fixed;inset:0;z-index:120;background:#0c0806eb;display:none;place-items:center;padding:20px}.lb.open{display:grid}.lb img{max-width:94vw;max-height:88vh;border-radius:8px;border:2px solid #fff}.lb button{position:absolute;top:18px;right:22px;background:none;border:0;color:#fff;font-size:1.8rem;cursor:pointer}\n"}],"routeData":{"route":"/galerie","isIndex":false,"type":"page","pattern":"^\\/galerie\\/?$","segments":[[{"content":"galerie","dynamic":false,"spread":false}]],"params":[],"component":"src/pages/galerie.astro","pathname":"/galerie","prerender":true,"fallbackRoutes":[],"distURL":[],"origin":"project","_meta":{"trailingSlash":"ignore"}}},{"file":"file:///home/user/knowledge-hub/atlas-asie/hotels/index.html","links":[],"scripts":[],"styles":[{"type":"external","src":"/atlas-asie/_astro/carnet.DqrDj1-l.css"},{"type":"inline","content":".intro{padding:clamp(30px,6vw,64px) 0 clamp(6px,2vw,18px)}.intro h1{font-size:clamp(2.6rem,8vw,5rem);margin:0 0 .6rem}.ht{padding:clamp(16px,3vw,32px) 0 clamp(40px,6vw,80px)}.hrow{background:var(--card);border:2px solid var(--ink);border-radius:14px;box-shadow:4px 4px 0 var(--ink);padding:16px 18px;margin:0 0 12px;display:grid;grid-template-columns:1fr auto;gap:12px 20px;align-items:start}.hrow .loc{font-size:.8rem;color:var(--muted);font-variant-numeric:tabular-nums}.hrow h3{font-family:var(--disp);text-transform:uppercase;font-size:clamp(1.15rem,2.6vw,1.6rem);margin:.15rem 0 .1rem}.hrow .adr{font-size:.86rem;color:var(--ink-soft)}.hrow .actions{display:flex;flex-direction:column;gap:8px;align-items:flex-end}.hrow .st{font-size:.62rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;padding:3px 9px;border-radius:999px;color:#fff;white-space:nowrap}.st--ok{background:var(--jade)}.st--todo{background:var(--gold);color:var(--ink)}.btn{display:inline-flex;align-items:center;gap:.4rem;font-weight:700;font-size:.8rem;border-radius:999px;padding:8px 14px;border:2px solid var(--ink);text-decoration:none;white-space:nowrap}.btn--map{background:var(--orange);color:#fff}.btn--book{background:transparent;color:var(--ink)}.btn svg{flex:none}.loading{color:var(--muted)}@media(max-width:560px){.hrow{grid-template-columns:1fr}.hrow .actions{flex-direction:row;align-items:center;justify-content:space-between}}\n"}],"routeData":{"route":"/hotels","isIndex":false,"type":"page","pattern":"^\\/hotels\\/?$","segments":[[{"content":"hotels","dynamic":false,"spread":false}]],"params":[],"component":"src/pages/hotels.astro","pathname":"/hotels","prerender":true,"fallbackRoutes":[],"distURL":[],"origin":"project","_meta":{"trailingSlash":"ignore"}}},{"file":"file:///home/user/knowledge-hub/atlas-asie/parcours/index.html","links":[],"scripts":[],"styles":[{"type":"external","src":"/atlas-asie/_astro/carnet.DqrDj1-l.css"},{"type":"inline","content":".intro{padding:clamp(30px,6vw,64px) 0 clamp(10px,3vw,24px)}.eyebrow{display:flex;align-items:center;gap:.6rem;font-weight:800;font-size:.76rem;letter-spacing:.16em;text-transform:uppercase;color:var(--orange-deep);margin:0 0 .4rem}.eyebrow:before{content:\"\";width:26px;height:3px;background:var(--orange)}.intro h1{font-size:clamp(2.6rem,8vw,5rem);margin:0 0 .6rem}.lead{color:var(--ink-soft);max-width:60ch;margin:0 0 1.2rem;font-size:1.05rem}.legend{display:flex;gap:1.4rem;flex-wrap:wrap;font-size:.82rem;color:var(--ink-soft)}.legend i.dot{display:inline-block;width:11px;height:11px;border-radius:50%;border:2px solid var(--ink);vertical-align:-1px;margin-right:.2rem}.dot.passe{background:var(--orange)}.dot.en-cours{background:var(--yellow)}.dot.a-venir{background:#fff}.tl{padding:clamp(20px,3vw,32px) 0 clamp(40px,6vw,80px)}.timeline{position:relative}.timeline:before{content:\"\";position:absolute;left:26px;top:8px;bottom:8px;width:3px;background:repeating-linear-gradient(var(--line) 0 10px,transparent 10px 18px)}.loading{color:var(--muted);padding-left:60px}.leg{position:relative;display:grid;grid-template-columns:56px 1fr;gap:clamp(14px,2.5vw,28px);padding:clamp(12px,2vw,20px) 0;scroll-margin-top:90px}.rail{position:relative;z-index:1;display:flex;flex-direction:column;align-items:center;gap:6px}.rail .node{width:20px;height:20px;border-radius:50%;border:3px solid var(--ink);background:#fff;margin-top:6px}.leg--passe .rail .node{background:var(--orange)}.leg--en-cours .rail .node{background:var(--yellow);box-shadow:0 0 #f3ea5db3;animation:pinpulse 1.8s infinite}.rail .ord{font-family:var(--disp);font-size:1.1rem;color:var(--muted)}.card{background:var(--card);border:2px solid var(--ink);border-radius:var(--r);box-shadow:var(--shadow);overflow:hidden;transition:transform .18s ease,box-shadow .18s ease}.card:hover{transform:translate(-2px,-2px);box-shadow:8px 8px 0 var(--orange)}.card .body{padding:clamp(16px,2.4vw,24px)}.chead{display:flex;align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap}.statut{font-size:.64rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase;padding:3px 10px;border-radius:999px;color:#fff}.statut.passe{background:var(--orange)}.statut.en-cours{background:var(--teal)}.statut.a-venir{background:var(--muted)}.wx{display:inline-flex;align-items:center;gap:.4rem;font-size:.85rem;color:var(--ink-soft);font-variant-numeric:tabular-nums}.wx svg{color:var(--orange-deep)}.card h2{font-family:var(--disp);font-size:clamp(1.4rem,3vw,2rem);text-transform:uppercase;margin:.5rem 0 .2rem}.cmeta{color:var(--muted);font-size:.86rem;font-variant-numeric:tabular-nums;margin-bottom:.7rem}.desc{color:var(--ink-soft);margin:0 0 1rem;max-width:66ch}.hotel{display:flex;gap:14px;align-items:flex-start;background:var(--peach);border:1px solid var(--line);border-radius:12px;padding:12px 14px}.hotel .hicon{color:var(--orange-deep);flex:none;margin-top:2px}.hotel .hnom{font-weight:700}.hotel .hadr{font-size:.84rem;color:var(--ink-soft)}.hotel a.hlink{font-size:.8rem;font-weight:700;color:var(--orange-deep);text-decoration:none;border-bottom:2px solid var(--yellow)}.hotel img{width:110px;height:80px;object-fit:cover;border-radius:8px;border:1px solid var(--line)}.media{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}.media img{width:120px;height:84px;object-fit:cover;border-radius:8px;border:1px solid var(--line)}.media a.vid{align-self:center;font-size:.82rem;font-weight:700;color:var(--orange-deep)}@media(max-width:560px){.leg{grid-template-columns:40px 1fr;gap:12px}.timeline:before{left:18px}.hotel img{display:none}}\n"}],"routeData":{"route":"/parcours","isIndex":false,"type":"page","pattern":"^\\/parcours\\/?$","segments":[[{"content":"parcours","dynamic":false,"spread":false}]],"params":[],"component":"src/pages/parcours.astro","pathname":"/parcours","prerender":true,"fallbackRoutes":[],"distURL":[],"origin":"project","_meta":{"trailingSlash":"ignore"}}},{"file":"file:///home/user/knowledge-hub/atlas-asie/pays/index.html","links":[],"scripts":[],"styles":[{"type":"external","src":"/atlas-asie/_astro/carnet.DqrDj1-l.css"},{"type":"external","src":"/atlas-asie/_astro/pays.CcnHs2W6.css"}],"routeData":{"route":"/pays","isIndex":false,"type":"page","pattern":"^\\/pays\\/?$","segments":[[{"content":"pays","dynamic":false,"spread":false}]],"params":[],"component":"src/pages/pays.astro","pathname":"/pays","prerender":true,"fallbackRoutes":[],"distURL":[],"origin":"project","_meta":{"trailingSlash":"ignore"}}},{"file":"file:///home/user/knowledge-hub/atlas-asie/trajets/index.html","links":[],"scripts":[],"styles":[{"type":"external","src":"/atlas-asie/_astro/carnet.DqrDj1-l.css"},{"type":"inline","content":".intro{padding:clamp(30px,6vw,64px) 0 clamp(6px,2vw,18px)}.intro h1{font-size:clamp(2.6rem,8vw,5rem);margin:0 0 .6rem}.tj{padding:clamp(16px,3vw,32px) 0 clamp(40px,6vw,80px)}.trip{display:grid;grid-template-columns:52px 1fr auto;gap:clamp(12px,2vw,20px);align-items:center;background:var(--card);border:2px solid var(--ink);border-radius:14px;box-shadow:4px 4px 0 var(--ink);padding:14px 16px;margin:0 0 12px}.trip .tico{width:44px;height:44px;border-radius:10px;display:grid;place-items:center;background:var(--peach);color:var(--orange-deep);border:1px solid var(--line)}.trip .mid .route{font-family:var(--disp);text-transform:uppercase;font-size:clamp(1rem,2.4vw,1.35rem);line-height:1}.trip .mid .route .arrow{color:var(--orange);margin:0 .3rem}.trip .mid .sub{font-size:.82rem;color:var(--ink-soft);margin-top:.35rem;font-variant-numeric:tabular-nums}.trip .mid .comp{color:var(--muted);font-size:.8rem;margin-top:.2rem}.trip .right{text-align:right}.trip .date{font-weight:700;font-size:.82rem;font-variant-numeric:tabular-nums}.trip .st{display:inline-block;margin-top:.4rem;font-size:.64rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;padding:3px 9px;border-radius:999px;color:#fff}.st--ok{background:var(--jade)}.st--todo{background:var(--gold);color:var(--ink)}.loading{color:var(--muted)}.taxi{grid-column:1 / -1;border-top:1px dashed var(--line);margin-top:4px;padding-top:8px}.taxi summary{cursor:pointer;font-size:.78rem;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--orange-deep);list-style:none;display:inline-flex;align-items:center;gap:.4rem}.taxi summary:before{content:\"🚕\";font-size:.95rem}.taxi summary:after{content:\"▾\";transition:transform .15s}.taxi[open] summary:after{transform:rotate(180deg)}.taxi-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;margin-top:10px}.apt{background:var(--peach);border:1px solid var(--line);border-radius:12px;padding:12px 14px}.apt-lbl{display:inline-block;font-size:.62rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-bottom:.3rem}.apt-en{font-weight:700;font-size:.92rem}.apt-adr{font-size:.8rem;color:var(--ink-soft);margin-top:.15rem}.apt-local{font-size:1.25rem;font-weight:600;margin-top:.45rem;line-height:1.3}.apt-btns{display:flex;gap:8px;margin-top:.65rem;flex-wrap:wrap}.btn-apt{display:inline-flex;align-items:center;gap:.35rem;font:700 .78rem var(--sans);border:2px solid var(--ink);border-radius:999px;padding:6px 12px;cursor:pointer;text-decoration:none}.btn-apt svg{width:14px;height:14px}.btn-apt--map{background:var(--orange);color:#fff}.btn-apt--copy{background:var(--card);color:var(--ink)}@media(max-width:560px){.trip{grid-template-columns:44px 1fr}.trip .right{grid-column:1 / -1;text-align:left;display:flex;gap:12px;align-items:center;justify-content:space-between}}\n"}],"routeData":{"route":"/trajets","isIndex":false,"type":"page","pattern":"^\\/trajets\\/?$","segments":[[{"content":"trajets","dynamic":false,"spread":false}]],"params":[],"component":"src/pages/trajets.astro","pathname":"/trajets","prerender":true,"fallbackRoutes":[],"distURL":[],"origin":"project","_meta":{"trailingSlash":"ignore"}}},{"file":"file:///home/user/knowledge-hub/atlas-asie/index.html","links":[],"scripts":[],"styles":[{"type":"external","src":"/atlas-asie/_astro/index.CIGW-MKW.css"},{"type":"external","src":"/atlas-asie/_astro/carnet.DqrDj1-l.css"},{"type":"external","src":"/atlas-asie/_astro/index.Bs1ru7SF.css"}],"routeData":{"route":"/","isIndex":true,"type":"page","pattern":"^\\/$","segments":[],"params":[],"component":"src/pages/index.astro","pathname":"/","prerender":true,"fallbackRoutes":[],"distURL":[],"origin":"project","_meta":{"trailingSlash":"ignore"}}}],"site":"https://hl-consulting.tech","base":"/atlas-asie","trailingSlash":"ignore","compressHTML":true,"componentMetadata":[["/home/user/knowledge-hub/atlas-asie-app/src/pages/carnet.astro",{"propagation":"none","containsHead":true}],["/home/user/knowledge-hub/atlas-asie-app/src/pages/galerie.astro",{"propagation":"none","containsHead":true}],["/home/user/knowledge-hub/atlas-asie-app/src/pages/hotels.astro",{"propagation":"none","containsHead":true}],["/home/user/knowledge-hub/atlas-asie-app/src/pages/index.astro",{"propagation":"none","containsHead":true}],["/home/user/knowledge-hub/atlas-asie-app/src/pages/parcours.astro",{"propagation":"none","containsHead":true}],["/home/user/knowledge-hub/atlas-asie-app/src/pages/pays.astro",{"propagation":"none","containsHead":true}],["/home/user/knowledge-hub/atlas-asie-app/src/pages/trajets.astro",{"propagation":"none","containsHead":true}]],"renderers":[],"clientDirectives":[["idle","(()=>{var l=(n,t)=>{let i=async()=>{await(await n())()},e=typeof t.value==\"object\"?t.value:void 0,s={timeout:e==null?void 0:e.timeout};\"requestIdleCallback\"in window?window.requestIdleCallback(i,s):setTimeout(i,s.timeout||200)};(self.Astro||(self.Astro={})).idle=l;window.dispatchEvent(new Event(\"astro:idle\"));})();"],["load","(()=>{var e=async t=>{await(await t())()};(self.Astro||(self.Astro={})).load=e;window.dispatchEvent(new Event(\"astro:load\"));})();"],["media","(()=>{var n=(a,t)=>{let i=async()=>{await(await a())()};if(t.value){let e=matchMedia(t.value);e.matches?i():e.addEventListener(\"change\",i,{once:!0})}};(self.Astro||(self.Astro={})).media=n;window.dispatchEvent(new Event(\"astro:media\"));})();"],["only","(()=>{var e=async t=>{await(await t())()};(self.Astro||(self.Astro={})).only=e;window.dispatchEvent(new Event(\"astro:only\"));})();"],["visible","(()=>{var a=(s,i,o)=>{let r=async()=>{await(await s())()},t=typeof i.value==\"object\"?i.value:void 0,c={rootMargin:t==null?void 0:t.rootMargin},n=new IntersectionObserver(e=>{for(let l of e)if(l.isIntersecting){n.disconnect(),r();break}},c);for(let e of o.children)n.observe(e)};(self.Astro||(self.Astro={})).visible=a;window.dispatchEvent(new Event(\"astro:visible\"));})();"]],"entryModules":{"\u0000@astro-page:src/pages/carnet@_@astro":"pages/carnet.astro.mjs","\u0000@astro-page:src/pages/galerie@_@astro":"pages/galerie.astro.mjs","\u0000@astro-page:src/pages/hotels@_@astro":"pages/hotels.astro.mjs","\u0000@astro-page:src/pages/index@_@astro":"pages/index.astro.mjs","\u0000@astro-page:src/pages/parcours@_@astro":"pages/parcours.astro.mjs","\u0000@astro-page:src/pages/pays@_@astro":"pages/pays.astro.mjs","\u0000@astro-page:src/pages/trajets@_@astro":"pages/trajets.astro.mjs","\u0000@astro-renderers":"renderers.mjs","\u0000noop-middleware":"_noop-middleware.mjs","\u0000virtual:astro:actions/noop-entrypoint":"noop-entrypoint.mjs","\u0000@astrojs-manifest":"manifest_COWvkTdU.mjs","/home/user/knowledge-hub/atlas-asie-app/src/components/Header.astro?astro&type=script&index=0&lang.ts":"_astro/Header.astro_astro_type_script_index_0_lang.BIq7qMyc.js","/home/user/knowledge-hub/atlas-asie-app/src/layouts/Base.astro?astro&type=script&index=0&lang.ts":"_astro/Base.astro_astro_type_script_index_0_lang.DZ9xzyaz.js","/home/user/knowledge-hub/atlas-asie-app/src/pages/galerie.astro?astro&type=script&index=0&lang.ts":"_astro/galerie.astro_astro_type_script_index_0_lang.Wg_-8Ibk.js","/home/user/knowledge-hub/atlas-asie-app/src/pages/hotels.astro?astro&type=script&index=0&lang.ts":"_astro/hotels.astro_astro_type_script_index_0_lang.BlqbvOP-.js","/home/user/knowledge-hub/atlas-asie-app/src/pages/index.astro?astro&type=script&index=0&lang.ts":"_astro/index.astro_astro_type_script_index_0_lang.BQpE_mWc.js","/home/user/knowledge-hub/atlas-asie-app/src/pages/parcours.astro?astro&type=script&index=0&lang.ts":"_astro/parcours.astro_astro_type_script_index_0_lang.DfBW_ixn.js","/home/user/knowledge-hub/atlas-asie-app/src/pages/pays.astro?astro&type=script&index=0&lang.ts":"_astro/pays.astro_astro_type_script_index_0_lang.qNz947tV.js","/home/user/knowledge-hub/atlas-asie-app/src/pages/trajets.astro?astro&type=script&index=0&lang.ts":"_astro/trajets.astro_astro_type_script_index_0_lang.Dhidyfya.js","astro:scripts/before-hydration.js":""},"inlinedScripts":[["/home/user/knowledge-hub/atlas-asie-app/src/components/Header.astro?astro&type=script&index=0&lang.ts","const e=document.getElementById(\"more-btn\"),n=document.getElementById(\"more-sheet\");e&&n&&(e.addEventListener(\"click\",t=>{t.stopPropagation();const a=n.classList.toggle(\"open\");e.setAttribute(\"aria-expanded\",String(a))}),document.addEventListener(\"click\",t=>{!n.contains(t.target)&&t.target!==e&&(n.classList.remove(\"open\"),[\"trajets\",\"carnet\",\"galerie\"].includes(document.body.dataset.active||\"\")||e.setAttribute(\"aria-expanded\",\"false\"))}));"],["/home/user/knowledge-hub/atlas-asie-app/src/layouts/Base.astro?astro&type=script&index=0&lang.ts","(function(){const e=document.getElementById(\"splash\");if(!e)return;const t=matchMedia(\"(prefers-reduced-motion:reduce)\").matches,n=()=>{e.classList.add(\"done\"),setTimeout(()=>e.remove(),700)};if(t||sessionStorage.getItem(\"amhe_splash\")){e.remove();return}sessionStorage.setItem(\"amhe_splash\",\"1\"),e.addEventListener(\"click\",n),setTimeout(n,3600)})();(function(){const e=document.getElementById(\"progress\");if(!e)return;const t=document.documentElement,n=()=>{const s=t.scrollHeight-t.clientHeight;e.style.width=(s>0?t.scrollTop/s*100:0)+\"%\"};addEventListener(\"scroll\",n,{passive:!0}),addEventListener(\"resize\",n),n()})();(function(){const e=document.querySelector('link[rel=\"manifest\"]')?.getAttribute(\"href\")?.replace(\"manifest.webmanifest\",\"\")||\"/\";\"serviceWorker\"in navigator&&navigator.serviceWorker.register(e+\"sw.js\").catch(()=>{});const t=()=>document.body.toggleAttribute(\"data-offline\",!navigator.onLine);addEventListener(\"online\",t),addEventListener(\"offline\",t),t()})();"]],"assets":["/atlas-asie/file:///home/user/knowledge-hub/atlas-asie/carnet/index.html","/atlas-asie/file:///home/user/knowledge-hub/atlas-asie/galerie/index.html","/atlas-asie/file:///home/user/knowledge-hub/atlas-asie/hotels/index.html","/atlas-asie/file:///home/user/knowledge-hub/atlas-asie/parcours/index.html","/atlas-asie/file:///home/user/knowledge-hub/atlas-asie/pays/index.html","/atlas-asie/file:///home/user/knowledge-hub/atlas-asie/trajets/index.html","/atlas-asie/file:///home/user/knowledge-hub/atlas-asie/index.html"],"i18n":{"fallbackType":"redirect","strategy":"pathname-prefix-other-locales","locales":["fr","en"],"defaultLocale":"fr","domainLookupTable":{}},"buildFormat":"directory","checkOrigin":false,"allowedDomains":[],"actionBodySizeLimit":1048576,"serverIslandNameMap":[],"key":"g5Eq10vK8tAQV4prxzIogdKVIkJcYUfm33GhJd+UlYU="});
if (manifest.sessionConfig) manifest.sessionConfig.driverModule = null;

export { manifest };
