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

import java.net.URISyntaxException;
import java.net.URL;
import org.junit.Test;

import com.xebialabs.overthere.OverthereFile;
import com.xebialabs.overthere.local.LocalConnection;
import com.xebialabs.overtherepy.DirectoryDiff;

import static org.hamcrest.CoreMatchers.equalTo;
import static org.hamcrest.CoreMatchers.notNullValue;
import static org.hamcrest.MatcherAssert.assertThat;

public class DirectoryDiffTest {

    private OverthereFile file(String name) throws URISyntaxException {
        URL resource = Thread.currentThread().getContextClassLoader().getResource(name);
        assertThat("File " + name + "not found", resource, notNullValue());
        return LocalConnection.getLocalConnection().getFile(resource.getPath());
    }

    @Test
    public void shouldDiffDirectories() throws Exception{

        OverthereFile leftDir = file("directorycompare/old");
        OverthereFile rightDir = file("directorycompare/new");

        DirectoryDiff diff = new DirectoryDiff(leftDir,rightDir);
        DirectoryDiff.DirectoryChangeSet changeSet = diff.diff();

        System.out.println("Changed files : " + changeSet.getChanged());
        assertThat(changeSet.getChanged().size(), equalTo(2));
        System.out.println("Removed files : " + changeSet.getRemoved());
        assertThat(changeSet.getRemoved().size(), equalTo(3));
        System.out.println("Added files : " + changeSet.getAdded());
        assertThat(changeSet.getAdded().size(), equalTo(3));




    }
}
