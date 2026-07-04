export type MockDocument = {
  id: string;
  title: string;
  template: string;
  status: 'draft' | 'exported';
  createdAt: string;
};

export const mockDocuments: MockDocument[] = [
  {
    id: 'doc_001',
    title: 'Propuesta para escuela privada',
    template: 'Propuesta comercial',
    status: 'draft',
    createdAt: '2026-07-04'
  },
  {
    id: 'doc_002',
    title: 'Plan de clase inicial',
    template: 'Plan de clase',
    status: 'draft',
    createdAt: '2026-07-04'
  }
];
