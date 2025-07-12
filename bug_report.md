# Bug Report - AI Hedge Fund Code Review

## Critical Issues Found

### 1. **Critical Bug: Undefined Variable Reference in main.py**
**Location**: `src/main.py:55`
**Severity**: High
**Issue**: The `app` variable is referenced but only defined within the `if __name__ == "__main__"` block (line 178). This causes a NameError when `run_hedge_fund` is called from other modules (like backtester.py) with `selected_analysts=None`.

**Impact**: The backtester will crash when trying to use default analysts.

**Fix**: Move the default workflow creation outside the main block or handle the case differently.

### 2. **Poor Exception Handling**
**Locations**: 
- `src/main.py:33` 
- `src/backtester.py:93`
**Severity**: Medium
**Issue**: Bare `except:` clauses catch all exceptions without proper error handling or logging.

**Impact**: Debugging becomes difficult as exceptions are silently swallowed.

**Fix**: Use specific exception handling and provide meaningful error messages.

### 3. **Typo in Help Text**
**Location**: `src/main.py:127`
**Severity**: Low
**Issue**: Extra closing parenthesis in the help text: `"Defaults to 100000.0)"`

**Impact**: Minor UI issue in command line help.

**Fix**: Remove the extra parenthesis.

### 4. **Hardcoded Tickers in Backtester**
**Location**: `src/backtester.py:364`
**Severity**: Medium
**Issue**: The line `tickers = ["AAPL"]` hardcodes the ticker and ignores the command line argument.

**Impact**: Users cannot specify custom tickers for backtesting.

**Fix**: Use the parsed command line argument instead.

## Recommendations

1. **Fix the critical undefined variable bug immediately** - this will prevent the app from running
2. **Improve exception handling** - add specific exception types and logging
3. **Fix the hardcoded ticker issue** - restore proper command line argument handling
4. **Add input validation** - ensure dates are valid and tickers are properly formatted
5. **Consider adding unit tests** - to catch these issues in the future

## Priority Order
1. Fix undefined variable bug (Critical)
2. Fix hardcoded tickers (Medium)
3. Improve exception handling (Medium)
4. Fix typo (Low)