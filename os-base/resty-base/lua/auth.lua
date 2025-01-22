local http = require("resty.http")
local openidc = require("resty.openidc")

local httpc = http.new()
httpc:set_timeouts(5000, 5000, 5000)  -- Set timeouts

-- Resolve using IPv4 and fetch OpenID Connect discovery document
local res, err = httpc:request_uri("https://orcid.org/.well-known/openid-configuration", {
    method = "GET",
    ssl_verify = false, -- Enable SSL verification
    options = {
        resolver = {
            nameserver = {"8.8.8.8"},  -- Use Google's IPv4 DNS resolver
            ipv4 = true,
        }
    }
})

if not res then
    ngx.log(ngx.ERR, "HTTP request to discovery URL failed: ", err)
    return ngx.exit(ngx.HTTP_INTERNAL_SERVER_ERROR)
end

-- Parse the discovery response (JSON)
local discovery_doc = res.body
ngx.log(ngx.INFO, "OpenID Connect discovery document fetched successfully.")

-- local openidc = require("resty.openidc")

local opts = {
    redirect_uri_path = "/callback",
    discovery = "https://orcid.org/.well-known/openid-configuration",
    client_id = "APP-YF13SGHMK800ZIHP",
    client_secret = "a79a7e96-9618-4c7b-91ef-0c5c54a2f0f1",
    scope = "openid email profile",
    ssl_verify = "no", -- Disable SSL verification (temporary)
}

-- Authenticate the request
local oidc_res, oidc_err = openidc.authenticate(opts)

if oidc_err then
    ngx.log(ngx.ERR, "Authentication failed: ", oidc_err)
    ngx.status = ngx.HTTP_FORBIDDEN
    ngx.say("Access denied: ", oidc_err)
    return ngx.exit(ngx.HTTP_FORBIDDEN)
end

-- Pass authenticated user information to the upstream service
ngx.req.set_header("X-User", oidc_res.id_token.sub)
ngx.req.set_header("X-User-Email", oidc_res.id_token.email or "")
ngx.req.set_header("X-User-Name", oidc_res.id_token.name or "")

-- Continue to the requested upstream location
ngx.status = ngx.HTTP_OK

