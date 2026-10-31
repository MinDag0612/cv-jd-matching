export default function HeroSection() {
  return (
    <section className="hero-section">
      <div className="container">
        <div className="row align-items-center g-5">
          <div className="col-lg-6">
            <p className="eyebrow">CÔNG CỤ HỖ TRỢ TUYỂN DỤNG</p>
            <h1>
              Tìm đúng người.
              <br />
              Chọn đúng cơ hội.
            </h1>
            <p className="hero-copy">
              Đối chiếu hồ sơ ứng viên với yêu cầu công việc một cách rõ ràng,
              để mỗi quyết định tuyển dụng bắt đầu bằng thông tin hữu ích.
            </p>
            <a className="btn btn-ink" href="#quy-trinh">
              Khám phá cách hoạt động
            </a>
            <p className="hero-note">Ít phỏng đoán hơn. Nhiều góc nhìn hơn.</p>
          </div>
          <div className="col-lg-6">
            <div className="match-illustration" aria-label="Minh họa đối chiếu CV và JD">
              <div className="doodle-label">MỌI THỨ BẮT ĐẦU TỪ SỰ RÕ RÀNG</div>
              <div className="document-pair">
                <div className="paper-card cv-paper">
                  <p className="paper-kicker">ỨNG VIÊN</p>
                  <h2>Hồ sơ</h2>
                  <span className="paper-line line-long" />
                  <span className="paper-line line-short" />
                  <span className="paper-line line-medium" />
                  <span className="paper-chip">Kinh nghiệm</span>
                </div>
                <div className="paper-card jd-paper">
                  <p className="paper-kicker">VỊ TRÍ</p>
                  <h2>Công việc</h2>
                  <span className="paper-line line-medium" />
                  <span className="paper-line line-long" />
                  <span className="paper-line line-short" />
                  <span className="paper-chip">Yêu cầu</span>
                </div>
              </div>
              <div className="match-sticker">
                <span>PHÙ HỢP</span>
                <strong>92%</strong>
              </div>
              <p className="illustration-caption">Minh họa quy trình phân tích</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
