import { headers } from 'next/headers';

export const isAuthenticated = () => {
  const foo = btoa('dfepassword');
  //console.dir(`Foo: ${foo}`);
  const authorization = headers().get('authorization');

  //console.dir(authorization);
  if (!authorization) {
    return false;
  }

  const authValue = authorization.split(' ')[1];
  console.dir(atob(authValue));
  console.dir(btoa('dfe:password'));
  const [username, password] = atob(authValue).split(':');

  return username == 'dfe' && password == process.env.AUTH_PASSWORD;
};
