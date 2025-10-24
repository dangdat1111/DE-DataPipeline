-- 1. Bảng USERS: Lưu trữ thông tin về tất cả các người dùng (Actor, Owner)
CREATE TABLE USERS (
    user_id BIGINT PRIMARY KEY, -- ID duy nhất của người dùng (từ GitHub)
    login VARCHAR(255) NOT NULL UNIQUE, -- Tên đăng nhập
    avatar_url VARCHAR(512),
    url VARCHAR(512),
    type VARCHAR(50), -- Ví dụ: 'User'
    site_admin BOOLEAN,
    -- Các trường khác từ API có thể thêm nếu cần
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

---

-- 2. Bảng REPOS: Lưu trữ thông tin về các kho lưu trữ (Repo gốc và Forkee)
CREATE TABLE REPOS (
    repo_id BIGINT PRIMARY KEY, -- ID duy nhất của kho lưu trữ (từ GitHub)
    name VARCHAR(255) NOT NULL,
    full_name VARCHAR(512) UNIQUE,
    url VARCHAR(512),
    html_url VARCHAR(512),
    description TEXT,
    is_private BOOLEAN,
    is_fork BOOLEAN,
    homepage VARCHAR(512),
    size INT,
    language VARCHAR(100),
    forks_count INT DEFAULT 0,
    stargazers_count INT DEFAULT 0,
    watchers_count INT DEFAULT 0,
    default_branch VARCHAR(100),
    created_at DATETIME,
    updated_at DATETIME,
    pushed_at DATETIME
);

---

-- 3. Bảng ORGS: Lưu trữ thông tin về các tổ chức (Org)
CREATE TABLE ORGS (
    org_id BIGINT PRIMARY KEY, -- ID duy nhất của tổ chức (từ GitHub)
    login VARCHAR(255) NOT NULL UNIQUE,
    url VARCHAR(512),
    avatar_url VARCHAR(512),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

---

-- 4. Bảng EVENTS: Lưu trữ thông tin cơ bản và chi tiết về sự kiện
CREATE TABLE EVENTS (
    event_id VARCHAR(50) PRIMARY KEY, -- ID sự kiện duy nhất
    event_type VARCHAR(100) NOT NULL, -- Ví dụ: 'ForkEvent'
    actor_id BIGINT, -- Khóa ngoại trỏ đến người thực hiện sự kiện
    repo_id BIGINT, -- Khóa ngoại trỏ đến kho lưu trữ gốc
    org_id BIGINT, -- Khóa ngoại trỏ đến tổ chức (có thể NULL)
    is_public BOOLEAN,
    created_at DATETIME NOT NULL,

    -- Thông tin chi tiết cho ForkEvent (đây là Forkee)
    forkee_repo_id BIGINT, -- Khóa ngoại trỏ đến kho lưu trữ mới được tạo (Forkee)

    FOREIGN KEY (actor_id) REFERENCES USERS(user_id) ON DELETE CASCADE,
    FOREIGN KEY (repo_id) REFERENCES REPOS(repo_id) ON DELETE CASCADE,
    FOREIGN KEY (org_id) REFERENCES ORGS(org_id) ON DELETE SET NULL,
    FOREIGN KEY (forkee_repo_id) REFERENCES REPOS(repo_id) ON DELETE CASCADE
);

---

-- 5. Bảng REPO_OWNERSHIP: Lưu trữ mối quan hệ sở hữu giữa Repo và User/Org
-- Bảng này giúp xử lý trường hợp Owner của Forkee (user_id) và Repo gốc (org_id)
CREATE TABLE REPO_OWNERSHIP (
    repo_id BIGINT,
    owner_user_id BIGINT NULL, -- Có thể là User sở hữu (OWNER của Forkee)
    owner_org_id BIGINT NULL, -- Hoặc là Org sở hữu (REPO gốc)

    PRIMARY KEY (repo_id), -- Mỗi repo chỉ có 1 chủ sở hữu chính

    FOREIGN KEY (repo_id) REFERENCES REPOS(repo_id) ON DELETE CASCADE,
    FOREIGN KEY (owner_user_id) REFERENCES USERS(user_id) ON DELETE SET NULL,
    FOREIGN KEY (owner_org_id) REFERENCES ORGS(org_id) ON DELETE SET NULL,

    -- Đảm bảo chỉ có một trong hai owner_id được điền
    CONSTRAINT chk_one_owner_type CHECK (owner_user_id IS NOT NULL OR owner_org_id IS NOT NULL)
);