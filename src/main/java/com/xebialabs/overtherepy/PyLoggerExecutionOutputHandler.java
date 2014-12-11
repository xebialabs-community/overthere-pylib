/**
 * Copyright (c) 2008-2014, XebiaLabs B.V., All rights reserved.
 *
 *
 * Overtherepy is licensed under the terms of the GPLv2
 * <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>, like most XebiaLabs Libraries.
 * There are special exceptions to the terms and conditions of the GPLv2 as it is applied to
 * this software, see the FLOSS License Exception
 * <http://github.com/xebialabs/overthere/blob/master/LICENSE>.
 *
 * This program is free software; you can redistribute it and/or modify it under the terms
 * of the GNU General Public License as published by the Free Software Foundation; version 2
 * of the License.
 *
 * This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
 * without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 * See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along with this
 * program; if not, write to the Free Software Foundation, Inc., 51 Franklin St, Fifth
 * Floor, Boston, MA 02110-1301  USA
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
