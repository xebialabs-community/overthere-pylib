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
