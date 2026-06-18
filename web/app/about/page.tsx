'use client';
import { useI18n } from '@/lib/i18n';

export default function AboutPage() {
  const { t } = useI18n();
  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">{t('about.title')}</h2>
      <div className="bg-white rounded-lg p-6 shadow">
        <p>{t('about.description')}</p>
      </div>
    </div>
  );
}
