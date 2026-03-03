# AWS Cloud Infrastructure - E-Commerce Platform

> A production-grade AWS cloud infrastructure project demonstrating scalability, security, and observability best practices.

---

## Architecture Overview

```
Internet Users
      ↓
  AWS WAF (Security)
      ↓
Application Load Balancer (Public Subnet)
      ↓
  ┌───┴───┐
  ↓       ↓
AZ-1     AZ-2
EC2      EC2
(Private Subnets)
      ↓
CloudWatch (Monitoring) + CloudTrail (Audit)
```

---

## Infrastructure Components

| Component | Details |
|-----------|---------|
| **VPC** | Custom VPC with public/private subnets across 2 AZs |
| **Load Balancer** | Application Load Balancer (Internet-facing) |
| **Auto Scaling** | Min: 1, Max: 3, CPU target: 70% |
| **WAF** | Managed rules + Rate limiting (2000 req/IP) |
| **CloudWatch** | Dashboard + Alarms + SNS notifications |
| **CloudTrail** | Full API audit logging |

---

## Security Features

- ✅ EC2 instances in **private subnets** (no direct internet access)
- ✅ **AWS WAF** blocking XSS, SQL Injection, and malicious bots
- ✅ **Security Groups** with least privilege access
- ✅ **CloudTrail** audit logging for compliance
- ✅ Load Balancer as single entry point

---

## Tech Stack

**Backend:** FastAPI, SQLAlchemy, Python 3.9, Uvicorn  
**Frontend:** HTML5, CSS3, Vanilla JavaScript  
**Server:** Nginx (Reverse Proxy), Systemd  
**Database:** SQLite  
**Infrastructure:** AWS EC2, ALB, ASG, WAF, VPC, CloudWatch, CloudTrail  

---

## Project Structure

```
clothing-store/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── add_sample_data.py   # Sample data script
├── frontend/
│   └── index.html           # Single page application
├── config/
│   ├── nginx.conf           # Nginx reverse proxy config
│   └── fastapi.service      # Systemd service file
├── screenshots/             # AWS Console screenshots
└── README.md
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/products/` | Get all products |
| POST | `/api/products/` | Create product |
| GET | `/api/products/{id}` | Get product by ID |
| PUT | `/api/products/{id}` | Update product |
| DELETE | `/api/products/{id}` | Delete product |
| GET | `/api/categories/` | Get all categories |
| POST | `/api/categories/` | Create category |
| GET | `/health` | Health check |

---

## Deployment Steps

### 1. Setup EC2 Instance
```bash
git clone https://github.com/yousefwaguih/clothing-store.git
cd clothing-store/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Nginx
```bash
sudo cp config/nginx.conf /etc/nginx/conf.d/clothing-store.conf
sudo systemctl restart nginx
```

### 3. Configure FastAPI Service
```bash
sudo cp config/fastapi.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable fastapi
sudo systemctl start fastapi
```

### 4. Add Sample Data
```bash
cd backend
python add_sample_data.py
```

---

## Monitoring

- **CloudWatch Dashboard:** CPU, Requests, Response Time, Healthy Hosts
- **Alarms:** SNS notification when CPU > 80%
- **WAF Logs:** Real-time attack monitoring

---

## Key Achievements

- Deployed scalable infrastructure handling automatic scaling based on CPU
- WAF successfully blocked real attacks during testing (XSS, bots)
- Implemented defense-in-depth with private subnets + WAF + Security Groups
- Full audit trail with CloudTrail logging all AWS API calls
- Zero-downtime deployments using Golden AMI strategy

---

*Note: The web application is intentionally simple — the focus of this project is cloud infrastructure architecture, security, and operations.*
