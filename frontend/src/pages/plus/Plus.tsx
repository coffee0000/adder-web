import React, { useState, useEffect } from "react";

const Plus = () => {
  const [num1, setNum1] = useState<string>("");
  const [num2, setNum2] = useState<string>("");
  const [result, setResult] = useState<number | null>(null);
  const [isHovered, setIsHovered] = useState<boolean>(false);
  const [isMenuOpen, setIsMenuOpen] = useState<boolean>(false);
  const [user, setUser] = useState<string | null>(null);


  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await fetch("/oauth2/userinfo", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });

        if (response.ok) {
          const data = await response.json();
          setUser(data.userinfo.name); 
        } else {
          console.error("Failed to fetch user info");
        }
      } catch (error) {
        console.error("Error fetching user info:", error);
      }
    };

    fetchUser();
  }, []);


  const handleLogout = async () => {
    localStorage.removeItem('access_token');
    sessionStorage.removeItem('access_token');
    window.location.href = '/oauth2/logout';
  };


  const handleMouseEnter = () => setIsHovered(true);
  const handleMouseLeave = () => setIsHovered(false);

  const handleCalculate = async () => {
    if (num1 === "" || num2 === "") {
      alert("Please enter valid numbers in both fields.");
      return;
    }

    const parsedNum1 = parseFloat(num1);
    const parsedNum2 = parseFloat(num2);

    if (isNaN(parsedNum1) || isNaN(parsedNum2)) {
      alert("Please enter valid numbers.");
      return;
    }

    try {
      const response = await fetch("/biz/calculate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          num1: parsedNum1,
          num2: parsedNum2,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResult(data.result);
    } catch (error) {
      console.error("Error calculating:", error);
      alert("Error calculating the result. Please try again.");
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.header}>Simple Calculator</h1>
      <div style={styles.calculator}>
        <input
          type="number"
          value={num1}
          onChange={(e) => setNum1(e.target.value)}
          placeholder="Enter first number"
          style={styles.input}
        />
        <span style={styles.symbol}>+</span>
        <input
          type="number"
          value={num2}
          onChange={(e) => setNum2(e.target.value)}
          placeholder="Enter second number"
          style={styles.input}
        />
        <button
          onClick={handleCalculate}
          style={{ ...styles.button, ...(isHovered ? styles.buttonHover : {}) }}
          onMouseEnter={handleMouseEnter}
          onMouseLeave={handleMouseLeave}
        >
          =
        </button>
        <div style={styles.resultText}>
          {result !== null ? `Result: ${result}` : "Result will appear here"}
        </div>
      </div>

      {/* 右上角的菜单按钮 */}
      <div style={styles.menuButtonContainer}>
        <button
          style={styles.menuButton}
          onClick={() => setIsMenuOpen((prev) => !prev)} // 切换菜单显示
        >
          ☰
        </button>

        {isMenuOpen && (
          <div style={styles.dropdownMenu}>
            <div style={styles.username}>{user ? `Hello, ${user}` : "Loading..."}</div>
            <button onClick={handleLogout} style={styles.logoutButton}>
              Logout
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  container: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    height: "100vh",
    background: "linear-gradient(to right, #f8c8d7, #ffafcc)",  // 更温柔的粉色渐变
    color: "#fff",
    fontFamily: "'Poppins', sans-serif",
  },
  header: {
    fontSize: "2.5rem",
    marginBottom: "25px",
    textShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
    fontWeight: "lighter",
  },
  calculator: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    background: "rgba(255, 255, 255, 0.8)",  // 半透明背景
    padding: "12px 25px",
    borderRadius: "30px",
    boxShadow: "0 4px 12px rgba(0, 0, 0, 0.1)",
  },
  input: {
    width: "90px",
    padding: "12px",
    fontSize: "1.2rem",
    borderRadius: "15px",
    border: "2px solid #ffb6c1",  // 更精致的粉色边框
    background: "#fff",
    color: "#ff69b4",  // 字体颜色稍微带有少女感
    textAlign: "center",
    outline: "none",
    margin: "0 12px",
    boxShadow: "0 2px 6px rgba(0, 0, 0, 0.1)",
    transition: "all 0.3s ease",
  },
  symbol: {
    fontSize: "2.2rem",
    margin: "0 12px",
    fontWeight: "bold",
    color: "#ff69b4",  // 使用更加少女感的粉色
    textShadow: "0 4px 6px rgba(0, 0, 0, 0.2)",
  },
  button: {
    background: "#ff69b4", // 更加少女的粉色
    color: "#fff",
    fontSize: "1.6rem",
    border: "none",
    borderRadius: "20px",
    padding: "12px 25px",
    cursor: "pointer",
    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
    transition: "background 0.3s ease, transform 0.2s ease",
  },
  buttonHover: {
    background: "#ff3385",
    transform: "scale(1.05)",
  },
  resultText: {
    fontSize: "1.5rem",
    color: "#ffb6c1",  // 结果文字使用粉色
    marginLeft: "25px",
    fontWeight: "bold",
    textShadow: "0 2px 4px rgba(0, 0, 0, 0.1)",
  },
  menuButtonContainer: {
    position: "absolute",
    top: "20px",
    right: "20px",
  },
  menuButton: {
    background: "#ff69b4",
    color: "#fff",
    fontSize: "2rem",
    border: "none",
    borderRadius: "50%",
    padding: "15px",
    cursor: "pointer",
    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
    transition: "background 0.3s ease, transform 0.2s ease",
  },
  dropdownMenu: {
    position: "absolute",
    top: "50px",
    right: "0",
    backgroundColor: "#fff",
    padding: "10px",
    borderRadius: "10px",
    boxShadow: "0 6px 18px rgba(0, 0, 0, 0.2)",
    width: "180px",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
  },
  username: {
    marginBottom: "10px",
    color: "#ff69b4",
    fontSize: "1.2rem",
  },
  logoutButton: {
    background: "#ff3385",
    color: "#fff",
    border: "none",
    borderRadius: "8px",
    padding: "10px 20px",
    cursor: "pointer",
    width: "100%",
  },
};

export default Plus;
