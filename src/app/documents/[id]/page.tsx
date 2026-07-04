import { AppShell } from '@/components/AppShell';
import { DocumentEditor } from '@/components/DocumentEditor';

export default function Page({ params }: { params: { id: string } }) {
  return (
    <AppShell>
      <DocumentEditor id={params.id} />
    </AppShell>
  );
}
