'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { supabase } from '@/lib/supabaseClient';

type AuthMode = 'login' | 'register';

export function AuthForm({ mode }: { mode: AuthMode }) {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const isLogin = mode === 'login';

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setMessage('Procesando...');

    const result = isLogin
      ? await supabase.auth.signInWithPassword({ email, password })
      : await supabase.auth.signUp({ email, password });

    if (result.error) {
      setMessage(result.error.message);
      return;
    }

    if (isLogin) {
      router.replace('/dashboard');
      return;
    }

    setMessage('Cuenta creada. Revisa tu correo si Supabase requiere confirmacion.');
  }

  return (
    <form className="auth-card" onSubmit={handleSubmit}>
      <p className="eyebrow">Forge Workspace</p>
      <h1>{isLogin ? 'Iniciar sesion' : 'Crear cuenta'}</h1>
      <p className="muted">Acceso inicial para el MVP de Documents AI.</p>

      <label className="field-label" htmlFor="email">Correo</label>
      <input id="email" className="input" value={email} onChange={(event) => setEmail(event.target.value)} type="email" required />

      <label className="field-label" htmlFor="password">Contrasena</label>
      <input id="password" className="input" value={password} onChange={(event) => setPassword(event.target.value)} type="password" required minLength={6} />

      <button className="primary-button full-width" type="submit">
        {isLogin ? 'Entrar' : 'Registrarme'}
      </button>

      {message ? <p className="muted">{message}</p> : null}

      <a className="auth-link" href={isLogin ? '/register' : '/login'}>
        {isLogin ? 'Crear cuenta nueva' : 'Ya tengo cuenta'}
      </a>
    </form>
  );
}
