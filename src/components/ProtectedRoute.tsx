'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { supabase } from '@/lib/supabaseClient';

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const [ready, setReady] = useState(false);

  useEffect(() => {
    async function checkSession() {
      const { data } = await supabase.auth.getSession();
      if (!data.session) {
        router.replace('/login');
        return;
      }
      setReady(true);
    }

    checkSession();
  }, [router]);

  if (!ready) {
    return <div className="loading-state">Verificando sesion...</div>;
  }

  return <>{children}</>;
}
