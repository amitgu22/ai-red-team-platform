import os
from fastapi import Header, HTTPException, Request


def _keys():
    raw=os.getenv('REDTEAM_API_KEYS','admin:change-me:admin,analyst:change-me-analyst:analyst')
    out={}
    for item in raw.split(','):
        parts=item.strip().split(':')
        if len(parts)>=3:
            role=':'.join(parts[2:])
            out[parts[1]]={'name':parts[0],'role':role}
    return out


def authenticate(request: Request, x_api_key: str | None = Header(default=None)):
    if request.url.path in ['/api/health','/docs','/openapi.json','/redoc']:
        return {'name':'anonymous','role':'system'}
    keys=_keys()
    # Dev mode can explicitly disable authentication; production should never do this.
    if os.getenv('AUTH_REQUIRED','true').lower()!='true':
        return {'name':'dev-user','role':'admin'}
    identity=keys.get(x_api_key or '')
    if not identity:
        raise HTTPException(status_code=401, detail='Valid X-API-Key required')
    request.state.identity=identity
    return identity


def require_role(*allowed):
    def checker(request: Request):
        identity=getattr(request.state,'identity',None)
        if not identity:
            raise HTTPException(status_code=401, detail='Authentication required')
        if identity['role'] not in allowed:
            raise HTTPException(status_code=403, detail='Insufficient role')
        return identity
    return checker
