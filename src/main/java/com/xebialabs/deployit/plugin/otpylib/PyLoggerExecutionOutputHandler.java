/**
 * THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
 * FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
 */

package com.xebialabs.deployit.plugin.otpylib;

import java.io.Closeable;
import java.util.Timer;
import java.util.TimerTask;

import com.xebialabs.overthere.OverthereExecutionOutputHandler;

public class PyLoggerExecutionOutputHandler implements OverthereExecutionOutputHandler, Closeable {

    public static final int FLUSH_DELAY_MS = 5000;
    public static final int FLUSH_CHECK_INTERVAL_MS = 2000;

    private static final Timer flushTimer = new Timer("AutoFlushTimer", true);

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
