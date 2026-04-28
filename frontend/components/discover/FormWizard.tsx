import { QuestionField } from "./QuestionField";

const sampleQuestions = [
  "What promise does this book make to the reader?",
  "What changes in the protagonist by the end?",
  "What feeling should the final page leave behind?",
];

export function FormWizard() {
  return (
    <section className="mx-auto flex w-full max-w-3xl flex-col gap-6">
      <div>
        <h1 className="text-3xl font-semibold">Creative Discovery Wizard</h1>
        <p className="text-slate-600">The full 25-question flow will be split across five pages.</p>
      </div>
      <div className="space-y-4 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        {sampleQuestions.map((question) => (
          <QuestionField key={question} label={question} />
        ))}
      </div>
    </section>
  );
}
