import ScoreGauge from "./ScoreGauge.jsx";

const categoryLabels = {
  skill: "Kỹ năng",
  education: "Học vấn",
  experience: "Kinh nghiệm",
  certificate: "Chứng chỉ",
  project: "Dự án",
};

const verdictLabels = {
  Matched: "Phù hợp",
  "Partially Matched": "Phù hợp một phần",
  "Not Matched": "Chưa phù hợp",
};

function verdictClass(value) {
  return value?.toLowerCase().replaceAll(" ", "-") ?? "partially-matched";
}

function MatchStatus({ value }) {
  return (
    <span className={`match-status match-status-${verdictClass(value)}`}>
      {verdictLabels[value] ?? value}
    </span>
  );
}

export default function MatchResults({ result }) {
  const categories = Object.entries(result.list_commend ?? {});
  const summaryDetails = categories.find(([, details]) => details.overall_reason)?.[1] ??
    categories[0]?.[1];
  const summaryVerdict = summaryDetails?.overall_prefix ?? "Partially Matched";

  return (
    <section className="results-section" aria-labelledby="results-title">
      <div className="results-heading">
        <div>
          <p className="eyebrow">PHÂN TÍCH ĐÃ HOÀN TẤT</p>
          <h2 id="results-title">Kết quả đối chiếu</h2>
        </div>
        <ScoreGauge score={Number(result.total_score)} />
      </div>

      <div className={`result-summary match-result-${verdictClass(summaryVerdict)}`}>
        <div className="result-summary-title">
          <h3>Nhận xét tổng quan</h3>
          <MatchStatus value={summaryVerdict} />
        </div>
        <p>
          {summaryDetails?.overall_reason ??
            "Chưa có nhận xét tổng quan từ kết quả phân tích."}
        </p>
      </div>

      <div className="category-results">
        {categories.map(([category, details]) => (
          <article
            className={`category-card match-result-${verdictClass(details.overall_prefix)}`}
            key={category}
          >
            <div className="category-card-heading">
              <h3>{categoryLabels[category] ?? category}</h3>
              <MatchStatus value={details.overall_prefix} />
            </div>
            {details.overall_reason && <p className="category-reason">{details.overall_reason}</p>}
            <div className="requirement-list">
              {(details.item_details ?? []).map((item, index) => (
                <div
                  className={`requirement-item match-result-${verdictClass(item.prefix)}`}
                  key={`${category}-${index}`}
                >
                  <div className="requirement-item-heading">
                    <strong>Yêu cầu {index + 1}</strong>
                    <MatchStatus value={item.prefix} />
                  </div>
                  <p className="requirement-text">{item.jd_requirement}</p>
                  <div className="evidence-grid">
                    <div>
                      <span>Bằng chứng từ hồ sơ</span>
                      <p>{item.matched_cv_evidence || "Chưa tìm thấy thông tin tương ứng."}</p>
                    </div>
                    <div>
                      <span>Phân tích</span>
                      <p>{item.reason}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
