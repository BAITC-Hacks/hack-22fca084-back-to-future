export type Selection = { measure_id: string; district_id?: string | null };
export type IndicatorValue = { indicator_id: string; value: string };
export type Measure = {
  id: string;
  name: string;
  direction: string;
  scope: "city" | "district";
  cost: number;
  lag: number;
  effects: IndicatorValue[];
};
export type District = {
  id: string;
  name: string;
  profile: string;
  population_share: string;
  indicators: IndicatorValue[];
};
export type Catalog = {
  version: string;
  budget: number;
  required_selections: number;
  max_per_direction: number;
  horizon: number;
  districts: District[];
  measures: Measure[];
  indicators: { id: string; name: string; direction: string; weight: string }[];
};
export type CityResult = {
  score: string;
  weighted_average: string;
  weakest_score: string;
  critical_count: number;
  districts: {
    district_id: string;
    score: string;
    indicators: IndicatorValue[];
  }[];
};
export type Evaluation = {
  selections: Selection[];
  spent: number;
  remaining: number;
  before: CityResult;
  after: CityResult;
  score_delta: string;
  district_changes: {
    district_id: string;
    before: string;
    after: string;
    delta: string;
  }[];
  changes: {
    district_id: string;
    indicator_id: string;
    before: string;
    after: string;
    delta: string;
  }[];
  contributions: {
    kind: "measure" | "synergy";
    measure_ids: string[];
    district_id: string;
    indicator_id: string;
    raw_delta: string;
  }[];
};
export type Issue = { code: string; message: string; measure_ids?: string[] };
export type Outcome = { issues: Issue[]; result: Evaluation | null };
export type CatalogResponse = { catalog: Catalog; baseline: CityResult };
export type Analysis = {
  summary: string;
  strengths: string[];
  risks: string[];
  consequences: string[];
  recommendations: string[];
};
export type AiResponse = {
  status: "success" | "unavailable" | "error" | "invalid";
  message: string;
  analysis: Analysis | null;
  evaluation: Outcome;
};
