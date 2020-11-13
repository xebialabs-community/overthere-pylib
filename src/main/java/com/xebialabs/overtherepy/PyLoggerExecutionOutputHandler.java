/**
 * Copyright 2020 XEBIALABS
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */
package com.xebialabs.overtherepy;

import java.io.Closeable;
import java.util.Timer;
import java.util.TimerTask;

import com.xebialabs.overthere.OverthereExecutionOutputHandler;

/**
 * Adapter that passes logging information from Overthere to a PyLogger implementation
 */
public class PyLoggerExecutionOutputHandler implements OverthereExecutionOutputHandler, Closeable {

    public static final int FLUSH_DELAY_MS = 5000;
    public static final int FLUSH_CHECK_INTERVAL_MS = 2000;

    private final Timer flushTimer = new Timer("AutoFlushTimer", true);

    private PyLogger pyLogger;
    private boolean stdout;
    private StringBuilder lineBuffer;
    private long flushAfter;
    private TimerTask flushTimerTask;

    PyLoggerExecutionOutputHandler(PyLogger pyLogger, boolean stdout) {
        this.pyLogger = pyLogger;
        this.stdout = stdout;
        this.lineBuffer = new StringBuilder();
        this.flushAfter = nextFlushTime();
        this.flushTimerTask = new TimerTask() {
            @Override
            public void run() {
                checkFlushNeeded();
            }
        };
        flushTimer.schedule(this.flushTimerTask, FLUSH_DELAY_MS, FLUSH_CHECK_INTERVAL_MS);
    }

    private static long nextFlushTime() {
        return System.currentTimeMillis() + FLUSH_DELAY_MS;
    }

    private synchronized void checkFlushNeeded() {
        if (flushAfter < System.currentTimeMillis()) {
            flushLineBuffer();
        }
    }

    @Override
    public final void handleLine(String line) {
        // no-op
    }

    @Override
    public final void handleChar(char c) {
        if (c != '\r' && c != '\n') {
            appendToLineBuffer(c);
        }
        if (c == '\n') {
            flushLineBuffer();
        }
    }

    private synchronized void appendToLineBuffer(char c) {
        lineBuffer.append(c);
    }

    private synchronized void flushLineBuffer() {
        if (lineBuffer.length() > 0) {
            flushLine(lineBuffer.toString());
            lineBuffer.setLength(0);
        }
        flushAfter = nextFlushTime();
    }

    private void flushLine(String buffer) {
        if (stdout) {
            pyLogger.info(buffer);
        } else {
            pyLogger.error(buffer);
        }
    }

    @Override
    public synchronized void close() {
        flushTimerTask.cancel();
    }

    public static PyLoggerExecutionOutputHandler sysoutHandler(PyLogger pyLogger) {
        return new PyLoggerExecutionOutputHandler(pyLogger, true);
    }

    public static PyLoggerExecutionOutputHandler syserrHandler(PyLogger pyLogger) {
        return new PyLoggerExecutionOutputHandler(pyLogger, false);
    }

}
